from django.shortcuts import redirect, render
from django.contrib import messages

from projet.models.ventes import Client, ClientType, Commande, CommandeStatus, ModePayement


def miels_list(request):
    from projet.models.productions import Miel
    from django.db.models import Sum
    
    # Get all miels with related data
    miels_queryset = Miel.objects.select_related(
        'miel_type', 'consommable_type', 'unite_mesure'
    ).prefetch_related(
        'miel_stock', 'miel_price_histories'
    ).all()
    
    miels_data = []
    for miel in miels_queryset:
        # Calculate current stock (sum of all stock entries)
        current_stock = miel.miel_stock.aggregate(total=Sum('added_quantity'))['total'] or 0
        
        # Get latest price
        latest_price_entry = miel.miel_price_histories.order_by('-created_at').first()
        current_price = latest_price_entry.price if latest_price_entry else 0.0
        
        # Check if stock is below alert threshold
        seuil_alerte = miel.consommable_type.seuil_alerte
        is_low_stock = current_stock <= seuil_alerte
        
        miel_dict = {
            'id': miel.id,
            'nom': f"{miel.miel_type.name} - {miel.consommable_type.name}",
            'type_miel': miel.miel_type.name,
            'conteneur': miel.consommable_type.name,
            'stock_actuel': current_stock,
            'prix_actuel': current_price,
            'unite_mesure': miel.unite_mesure.name,
            'quantite_unite': miel.quantite_unite,
            'seuil_alerte': seuil_alerte,
            'is_low_stock': is_low_stock,
            'miel_stock': miel.miel_stock,
            'miel_price_histories': miel.miel_price_histories
        }
        miels_data.append(miel_dict)
    
    return render(request, "commerce/miels/list.html", {'miels': miels_data})


def clients_list(request):
    clientModels = Client.objects.prefetch_related("commandes", "ventes").all()
    clients = [
        {
            'id': client.id,
            'nom': client.name,
            'email': client.email,
            'type': client.client_type.name if client.client_type else '-',
            'telephone': client.contact,
            'derniere_commande': client.get_last_commande,
        } for client in clientModels
    ]
    return render(request, "commerce/clients/list.html", {"clients": clients})


def commandes_list(request):
    # Get all commandes with related data
    commandes_queryset = Commande.objects.prefetch_related(
        'commande_details__miel',
        'commande_status_histories__commande_status',
        'client'
    ).select_related('client', 'vente').all()
    
    # Get current status for each commande (latest status)
    commandes_data = []
    for commande in commandes_queryset:
        # Get the latest status
        latest_status = commande.commande_status_histories.order_by('-created_at').first()
        current_status = latest_status.commande_status.name if latest_status else 'Non défini'
        
        # Calculate total quantity from commande details
        total_quantity = sum(detail.quantite for detail in commande.commande_details.all())
        
        # Get first product name for display (or concatenate multiple)
        product_names = [detail.miel.miel_type.name for detail in commande.commande_details.all()]
        product_display = ', '.join(product_names) if product_names else 'Aucun produit'
        
        commande_dict = {
            'id': commande.id,
            'date': commande.created_at.strftime('%Y-%m-%d'),
            'client': commande.client.name,
            'produit': product_display,
            'quantite': total_quantity,
            'statut': current_status,
            'vente_id': commande.vente.id if commande.vente else None,
            'created_at': commande.created_at.strftime('%Y-%m-%d'),
            'livraison_date': commande.livraison_date.strftime('%Y-%m-%d'),
            'note': commande.note,
            'commande_details': commande.commande_details,
            'commande_status_histories': commande.commande_status_histories
        }
        commandes_data.append(commande_dict)

    # Separate commandes by status
    commandes_en_attente = [
        cmd for cmd in commandes_data 
        if cmd['statut'] in ['En attente', 'Créée', 'En préparation'] or cmd['vente_id'] is None
    ]

    commandes_livrees = [
        cmd for cmd in commandes_data 
        if cmd['statut'] in ['Livrée', 'Terminée'] or cmd['vente_id'] is not None
    ]

    return render(request, "commerce/commandes/list.html", {
        "commandes_en_attente": commandes_en_attente,
        "commandes_livrees": commandes_livrees,
    })


def ventes_list(request):
    from projet.models.ventes import Vente
    from django.db.models import Sum
    
    # Get all ventes with related data
    ventes_queryset = Vente.objects.prefetch_related(
        'vente_details__miel__miel_price_histories',
        'client',
        'commande'
    ).select_related('client').all()
    
    ventes_data = []
    for vente in ventes_queryset:
        # Calculate total quantity from vente details
        total_quantity = vente.vente_details.aggregate(total=Sum('quantite'))['total'] or 0
        
        # Get first product name for display (or concatenate multiple)
        product_names = [detail.miel.miel_type.name for detail in vente.vente_details.all()]
        product_display = ', '.join(product_names) if product_names else 'Aucun produit'
        
        # Calculate total amount
        total_amount = sum(
            detail.quantite * detail.miel.prix_unitaire 
            for detail in vente.vente_details.all()
        )
        
        vente_dict = {
            'id': vente.id,
            'date': vente.created_at.strftime('%Y-%m-%d'),
            'client': vente.client.name,
            'produit': product_display,
            'quantite': total_quantity,
            'montant': total_amount,
            'mode_payement': vente.mode_payement,
            'note': vente.note,
            'created_at': vente.created_at.strftime('%Y-%m-%d'),
            'vente_details': vente.vente_details,
            'commande': vente.commande
        }
        ventes_data.append(vente_dict)

    return render(request, "commerce/ventes/list.html", {
        "ventes": ventes_data
    })

def stock_miels_list(request):
    from projet.models.productions import Miel, MielStock, MielPriceHistory
    from django.db.models import Sum
    from datetime import datetime, date
    
    # Get selected date from request or use today
    selected_date = request.GET.get('date', date.today().strftime('%Y-%m-%d'))
    try:
        filter_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
    except ValueError:
        filter_date = date.today()
        selected_date = filter_date.strftime('%Y-%m-%d')
    
    # Get all miels with related data
    miels_queryset = Miel.objects.select_related(
        'miel_type', 'consommable_type', 'unite_mesure'
    ).prefetch_related(
        'miel_stock', 'miel_price_histories'
    ).all()
    
    miels_data = []
    for miel in miels_queryset:
        # Calculate current stock (sum of all stock entries up to selected date)
        stock_entries = miel.miel_stock.filter(created_at__date__lte=filter_date)
        current_stock = stock_entries.aggregate(total=Sum('added_quantity'))['total'] or 0
        
        # Get latest price up to selected date
        latest_price_entry = miel.miel_price_histories.filter(
            created_at__date__lte=filter_date
        ).order_by('-created_at').first()
        current_price = latest_price_entry.price if latest_price_entry else 0.0
        
        # Check if stock is below alert threshold
        seuil_alerte = miel.consommable_type.seuil_alerte
        is_low_stock = current_stock <= seuil_alerte
        
        miel_dict = {
            'id': miel.id,
            'nom': f"{miel.miel_type.name} - {miel.consommable_type.name}",
            'type_miel': miel.miel_type.name,
            'conteneur': miel.consommable_type.name,
            'stock_actuel': current_stock,
            'prix_actuel': current_price,
            'unite_mesure': miel.unite_mesure.name,
            'quantite_unite': miel.quantite_unite,
            'seuil_alerte': seuil_alerte,
            'is_low_stock': is_low_stock,
            'miel_stock': miel.miel_stock,
            'miel_price_histories': miel.miel_price_histories
        }
        miels_data.append(miel_dict)
    
    return render(request, "commerce/miels/stock.html", {
        "miels": miels_data,
        "selected_date": selected_date
    })

def stock_miels_form(request):
    from projet.models.productions import Miel, MielStock, MielPriceHistory
    from django.contrib import messages
    
    if request.method == "POST":
        # Handle form submission
        miel_id = request.POST.get('miel')
        operation_type = request.POST.get('type')
        quantity = request.POST.get('quantity')
        date = request.POST.get('date')
        
        try:
            # Validate inputs
            if not all([miel_id, operation_type, quantity, date]):
                messages.error(request, 'Tous les champs sont obligatoires.')
                raise ValueError("Missing required fields")
            
            miel = Miel.objects.get(id=miel_id)
            quantity_int = int(quantity)
            
            if quantity_int <= 0:
                messages.error(request, 'La quantité doit être supérieure à 0.')
                raise ValueError("Invalid quantity")
            
            # Calculate quantity based on operation type
            if operation_type == 'Sortie':
                added_quantity = -quantity_int
            else:
                added_quantity = quantity_int
            
            # Create stock entry
            MielStock.objects.create(
                miel=miel,
                added_quantity=added_quantity,
                created_at=date if date else None
            )
            
            # Success message
            operation_text = "sortie" if operation_type == 'Sortie' else "entrée"
            messages.success(request, f'Mouvement de stock enregistré avec succès : {operation_text} de {quantity_int} unités pour {miel.miel_type.name}.')
            
            return redirect('stock_miels_list')
            
        except Miel.DoesNotExist:
            messages.error(request, 'Le miel sélectionné n\'existe pas.')
        except ValueError as e:
            if "Invalid quantity" not in str(e) and "Missing required fields" not in str(e):
                messages.error(request, 'Veuillez vérifier les données saisies.')
        except Exception as e:
            messages.error(request, 'Une erreur inattendue s\'est produite. Veuillez réessayer.')
    
    # GET request - show form
    miels = Miel.objects.select_related('miel_type', 'consommable_type').all()
    
    miels_data = []
    for miel in miels:
        miels_data.append({
            'id': miel.id,
            'nom': f"{miel.miel_type.name} - {miel.consommable_type.name}",
        })
    
    return render(request, "commerce/miels/stock_form.html", {
        "miels": miels_data
    })

def client_vue(request):
    if request.method == "GET" or (request.POST and not request.POST.get('modify', None)):
        client_id = request.GET.get('id', None)

        if not client_id:
            return redirect('clients_list')

        client_model = Client.objects.filter(id=client_id).first()

        if not client_model:
            return redirect('clients_list')

        client = {
            'id': client_model.id,
            'nom': client_model.name,
            'note': client_model.note,
            'email': client_model.email,
            'telephone': client_model.contact,
            'adresse': client_model.adresse,
            'client_type': client_model.client_type.name if client_model.client_type else '-'
        }

        client_types = [
            {
                "id": client_type.id,
                "type": client_type.name
            } for client_type in ClientType.objects.all()
        ]
        return render(request, "commerce/clients/vue.html", {"client": client, "client_types": client_types})
    else:
        client_id = request.POST.get('id', None)

        if not client_id:
            return redirect('clients_list')

        client_model = Client.objects.filter(id=client_id).first()

        if not client_model:
            return redirect('clients_list')

        client = {
            'id': request.POST.get('id', client_model.id),
            'nom': request.POST.get('nom', client_model.name),
            'note': request.POST.get('note', client_model.note),
            'email': request.POST.get('email', client_model.email),
            'contact': request.POST.get('telephone', client_model.contact),
            'adresse': request.POST.get('adresse', client_model.adresse),
            'client_type': request.POST.get('client_type', client_model.client_type.name if client_model.client_type else None),
        }

        # Check if client_type is valid
        if not client['client_type']:
            print("Client type is not provided or invalid.")
            return redirect('client_form')

        try:
            client['client_type'] = ClientType.objects.get(
                name=client['client_type'])
        except ClientType.DoesNotExist:
            print("Client type does not exist.")
            return redirect('client_form')

        # Update client
        client_model.name = client['nom']
        client_model.note = client['note']
        client_model.email = client['email']
        client_model.contact = client['contact']
        client_model.adresse = client['adresse']
        client_model.client_type = client['client_type']

        client_model.save()

        return redirect('clients_list')

def client_form(request):
    if request.method == "POST":
        return client_create(request)
    client_types = [
        {
            "id": client_type.id,
            "type": client_type.name
        } for client_type in ClientType.objects.all()
    ]
    return render(request, "commerce/clients/form.html", {"client_types": client_types})

def client_create(request):
    if request.method == "POST":
        client = {
            'name': request.POST.get('nom', ''),
            'note': request.POST.get('note', ''),
            'email': request.POST.get('email', ''),
            'contact': request.POST.get('telephone', ''),
            'adresse': request.POST.get('adresse', ''),
            'client_type': request.POST.get('client_type', None),
        }

        # Check if client_type is valid
        if not client['client_type']:
            return redirect('client_form')
        try:
            client['client_type'] = ClientType.objects.get(
                name=client['client_type'])
        except ClientType.DoesNotExist:
            return redirect('client_form')

        Client.objects.create(
            name=client['name'],
            note=client['note'],
            email=client['email'],
            contact=client['contact'],
            adresse=client['adresse'],
            client_type=client['client_type']
        )

        pass
    return redirect('clients_list')

def vente_vue(request):
    if request.method == "GET":
        vente_id = request.GET.get('id', None)
        
        if not vente_id:
            return redirect('ventes_list')
        
        try:
            from projet.models.ventes import Vente
            vente_model = Vente.objects.prefetch_related(
                'vente_details__miel__miel_type',
                'client'
            ).select_related('client').get(id=vente_id)
        except Vente.DoesNotExist:
            return redirect('ventes_list')
        
        # Calculate total from details
        total_amount = sum(
            detail.quantite * detail.prix_unitaire 
            for detail in vente_model.vente_details.all()
        )
        
        # Get first product for main display
        first_product = vente_model.vente_details.first()
        product_display = first_product.miel.miel_type.name if first_product else 'Aucun produit'
        
        vente = {
            'id': vente_model.id,
            'miel': product_display,
            'client': vente_model.client.name,
            'mode_payement': vente_model.mode_payement,
            'note': vente_model.note,
            'date': vente_model.created_at.strftime('%Y-%m-%d'),
            'quantite': sum(detail.quantite for detail in vente_model.vente_details.all()),
            'montant': total_amount,
        }
        
        # Get dropdown options
        from projet.models.productions import Miel
        miels = Miel.objects.select_related('miel_type', 'consommable_type').all()
        clients = Client.objects.all()
        
        modes_payement = [
            {
                'id': mode.id,
                'mode': mode.name
            } for mode in ModePayement.objects.all()
        ]
        
        return render(request, "commerce/ventes/vue.html", {
            "vente": vente,
            "vente_model": vente_model,
            "modes_payement": modes_payement,
            "clients": clients,
            "miels": miels
        })
    
    elif request.method == "POST":
        vente_id = request.POST.get('id', None)
        
        if not vente_id:
            return redirect('ventes_list')
        
        try:
            from projet.models.ventes import Vente
            vente_model = Vente.objects.get(id=vente_id)
        except Vente.DoesNotExist:
            return redirect('ventes_list')
        
        # Update vente
        mode_payement = request.POST.get('mode_payement', vente_model.mode_payement.name)
        try:
            mode_payement_model = ModePayement.objects.get(name=mode_payement)
            vente_model.mode_payement = mode_payement_model
        except ModePayement.DoesNotExist:
            messages.error(request, 'Mode de paiement invalide.')
            return redirect('vente_vue', id=vente_id)
        
        vente_model.note = request.POST.get('note', vente_model.note)
        
        # Update client if changed
        client_id = request.POST.get('client')
        if client_id:
            try:
                client = Client.objects.get(id=client_id)
                vente_model.client = client
            except Client.DoesNotExist:
                pass
        
        vente_model.save()
        
        return redirect('ventes_list')

def vente_form(request):
    from projet.models.productions import Miel
    from projet.models.ventes import Vente, VenteDetail
    
    if request.method == "POST":
        # Handle form submission
        client_id = request.POST.get('client')
        mode_payement = request.POST.get('mode_payement')
        note = request.POST.get('note', '')
        
        # Get client
        try:
            client = Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            return redirect('vente_form')
        
        mode_payement_model = ModePayement.objects.filter(name=mode_payement).first()
        
        if not mode_payement_model:
            messages.error(request, 'Mode de paiement invalide.')
            return redirect('vente_form')    
    
        # Create vente
        vente = Vente.objects.create(
            client=client,
            mode_payement=mode_payement_model,
            note=note
        )
        
        # Process cart items
        cart_items = request.POST.getlist('cart_items')
        for item in cart_items:
            if item:  # Skip empty items
                print(item)
                divided = item.split('|')
                miel_id, quantite = divided[0], divided[1]
                try:
                    miel = Miel.objects.get(id=miel_id)
                    VenteDetail.objects.create(
                        vente=vente,
                        miel=miel,
                        quantite=int(quantite),
                    )
                except (Miel.DoesNotExist, ValueError):
                    continue
        
        return redirect('ventes_list')
    
    # GET request - show form
    clients = Client.objects.all().values('id', 'name')
    miels = Miel.objects.select_related('miel_type', 'consommable_type', 'unite_mesure').all()
    
    miels_data = []
    for miel in miels:
        # Get latest price
        latest_price = miel.miel_price_histories.order_by('-created_at').first()
        price = latest_price.price if latest_price else 0.0
        
        miels_data.append({
            'id': miel.id,
            'nom': f"{miel.miel_type.name} - {miel.consommable_type.name}",
            'prix': price,
            'unite': miel.unite_mesure.name,
            'quantite_unite': miel.quantite_unite
        })
        
    modes_payements = ModePayement.objects.all()
    
    modes_payement = [
        {'mode': mode.name} for mode in modes_payements
    ]
    
    return render(request, "commerce/ventes/form.html", {
        "clients": clients,
        "miels": miels_data,
        "modes_payement": modes_payement
    })

def commandes_stats(request):
    from projet.models.ventes import Commande, CommandeDetail, CommandeStatusHistory
    from projet.models.productions import Miel, MielType
    from django.db.models import Sum, Count, F, Q, Case, When, Value, IntegerField
    from django.db.models.functions import TruncDate
    from collections import defaultdict
    import json
    
    # Get all commandes with their latest status
    commandes = Commande.objects.prefetch_related(
        'commande_details__miel__miel_type',
        'commande_status_histories__commande_status',
        'client'
    ).all()
    
    # Group statistics by miel type
    stats_par_type = defaultdict(lambda: {
        'total_commandes': 0,
        'commandes_livrees': 0,
        'commandes_annulees': 0,
        'taux_livraison': 0.0,
        'ca_estime': 0.0,
        'repartition_par_jour': defaultdict(int),
        'top_clients': defaultdict(int)
    })
    
    # Calculate statistics for each commande
    for commande in commandes:
        # Get latest status
        latest_status = commande.commande_status_histories.order_by('-created_at').first()
        current_status = latest_status.commande_status.name if latest_status else 'Non défini'
        
        # Get all miel types in this commande
        for detail in commande.commande_details.all():
            miel_type = detail.miel.miel_type.name
            
            stats_par_type[miel_type]['total_commandes'] += 1
            
            # Count by status
            if current_status in ['Livrée', 'Terminée']:
                stats_par_type[miel_type]['commandes_livrees'] += 1
                # Calculate estimated revenue
                prix_unitaire = detail.miel.prix_unitaire
                stats_par_type[miel_type]['ca_estime'] += detail.quantite * prix_unitaire
            elif current_status == 'Annulée':
                stats_par_type[miel_type]['commandes_annulees'] += 1
            
            # Count by day
            date_str = commande.created_at.strftime('%Y-%m-%d')
            stats_par_type[miel_type]['repartition_par_jour'][date_str] += 1
            
            # Count by client
            stats_par_type[miel_type]['top_clients'][commande.client.name] += 1
    
    # Calculate delivery rates and format top clients
    for miel_type in stats_par_type:
        data = stats_par_type[miel_type]
        if data['total_commandes'] > 0:
            data['taux_livraison'] = data['commandes_livrees'] / data['total_commandes']
        
        # Get top 3 clients
        top_clients = sorted(data['top_clients'].items(), key=lambda x: x[1], reverse=True)[:3]
        data['top_clients'] = [client[0] for client in top_clients]
        
        # Convert defaultdict to regular dict
        data['repartition_par_jour'] = dict(data['repartition_par_jour'])
    
    # Convert to regular dict for template
    stats_par_type = dict(stats_par_type)
    
    # Calculate global statistics
    total_commandes = sum(data['total_commandes'] for data in stats_par_type.values())
    total_livrees = sum(data['commandes_livrees'] for data in stats_par_type.values())
    total_annulees = sum(data['commandes_annulees'] for data in stats_par_type.values())
    total_ca = sum(data['ca_estime'] for data in stats_par_type.values())
    
    stats_globales = {
        'total_commandes': total_commandes,
        'commandes_livrees': total_livrees,
        'commandes_annulees': total_annulees,
        'taux_livraison': total_livrees / total_commandes if total_commandes > 0 else 0,
        'ca_estime': total_ca,
        'produit_plus_vendu': max(stats_par_type.keys(), key=lambda x: stats_par_type[x]['total_commandes']) if stats_par_type else '',
        'client_fidele': '',  # Would need more complex calculation
        'courbe_jour_labels': [],
        'courbe_jour_valeurs': []
    }
    
    # Calculate global daily distribution
    all_dates = defaultdict(int)
    for data in stats_par_type.values():
        for date, count in data['repartition_par_jour'].items():
            all_dates[date] += count
    
    if all_dates:
        sorted_dates = sorted(all_dates.items())
        stats_globales['courbe_jour_labels'] = [date for date, _ in sorted_dates]
        stats_globales['courbe_jour_valeurs'] = [count for _, count in sorted_dates]
    
    return render(request, "commerce/commandes/stats.html", {
        "stats_par_type": stats_par_type,
        "stats_globales": stats_globales
    })


def miel_form(request):
    from projet.models.productions import Miel, MielType, MielPriceHistory
    from projet.models.ressources import ConsommableType, UniteMesure
    from django.contrib import messages
    
    if request.method == "POST":
        # Handle form submission
        miel_type_id = request.POST.get('miel_type')
        consommable_type_id = request.POST.get('consommable_type')
        unite_mesure_id = request.POST.get('unite_mesure')
        quantite_unite = request.POST.get('quantite_unite')
        prix_initial = request.POST.get('prix_initial')
        
        try:
            # Validate inputs
            if not all([miel_type_id, consommable_type_id, unite_mesure_id, quantite_unite]):
                messages.error(request, 'Tous les champs obligatoires doivent être remplis.')
                raise ValueError("Missing required fields")
            
            # Get model instances
            miel_type = MielType.objects.get(id=miel_type_id)
            consommable_type = ConsommableType.objects.get(id=consommable_type_id)
            unite_mesure = UniteMesure.objects.get(id=unite_mesure_id)
            
            quantite_unite_int = int(quantite_unite)
            if quantite_unite_int <= 0:
                messages.error(request, 'La quantité par unité doit être supérieure à 0.')
                raise ValueError("Invalid quantity")
            
            # Create miel
            miel = Miel.objects.create(
                miel_type=miel_type,
                consommable_type=consommable_type,
                unite_mesure=unite_mesure,
                quantite_unite=quantite_unite_int
            )
            
            # Create initial price if provided
            if prix_initial:
                try:
                    prix_float = float(prix_initial)
                    if prix_float > 0:
                        MielPriceHistory.objects.create(
                            miel=miel,
                            price=prix_float
                        )
                except ValueError:
                    pass  # Ignore invalid price, not required
            
            # Success message
            messages.success(request, f'Miel "{miel_type.name} - {consommable_type.name}" créé avec succès.')
            
            return redirect('miels_list')
            
        except (MielType.DoesNotExist, ConsommableType.DoesNotExist, UniteMesure.DoesNotExist):
            messages.error(request, 'Une des sélections n\'est pas valide.')
        except ValueError as e:
            if "Invalid quantity" not in str(e) and "Missing required fields" not in str(e):
                messages.error(request, 'Veuillez vérifier les données saisies.')
        except Exception as e:
            messages.error(request, 'Une erreur inattendue s\'est produite. Veuillez réessayer.')
    
    # GET request - show form
    miel_types = MielType.objects.all()
    consommable_types = ConsommableType.objects.select_related('unite').all()
    unite_mesures = UniteMesure.objects.all()
    from projet.models.productions import Miel, MielType, MielPriceHistory
    from projet.models.ressources import ConsommableType, UniteMesure
    from django.contrib import messages
    
    if request.method == "POST":
        # Handle form submission
        miel_type_id = request.POST.get('miel_type')
        consommable_type_id = request.POST.get('consommable_type')
        unite_mesure_id = request.POST.get('unite_mesure')
        quantite_unite = request.POST.get('quantite_unite')
        prix_initial = request.POST.get('prix_initial')
        
        try:
            # Validate inputs
            if not all([miel_type_id, consommable_type_id, unite_mesure_id, quantite_unite]):
                messages.error(request, 'Tous les champs obligatoires doivent être remplis.')
                raise ValueError("Missing required fields")
            
            # Get model instances
            miel_type = MielType.objects.get(id=miel_type_id)
            consommable_type = ConsommableType.objects.get(id=consommable_type_id)
            unite_mesure = UniteMesure.objects.get(id=unite_mesure_id)
            
            quantite_unite_int = int(quantite_unite)
            if quantite_unite_int <= 0:
                messages.error(request, 'La quantité par unité doit être supérieure à 0.')
                raise ValueError("Invalid quantity")
            
            # Create miel
            miel = Miel.objects.create(
                miel_type=miel_type,
                consommable_type=consommable_type,
                unite_mesure=unite_mesure,
                quantite_unite=quantite_unite_int
            )
            
            # Create initial price if provided
            if prix_initial:
                try:
                    prix_float = float(prix_initial)
                    if prix_float > 0:
                        MielPriceHistory.objects.create(
                            miel=miel,
                            price=prix_float
                        )
                except ValueError:
                    pass  # Ignore invalid price, not required
            
            # Success message
            messages.success(request, f'Miel "{miel_type.name} - {consommable_type.name}" créé avec succès.')
            
            return redirect('miels_list')
            
        except (MielType.DoesNotExist, ConsommableType.DoesNotExist, UniteMesure.DoesNotExist):
            messages.error(request, 'Une des sélections n\'est pas valide.')
        except ValueError as e:
            if "Invalid quantity" not in str(e) and "Missing required fields" not in str(e):
                messages.error(request, 'Veuillez vérifier les données saisies.')
        except Exception as e:
            messages.error(request, 'Une erreur inattendue s\'est produite. Veuillez réessayer.')
    
    # GET request - show form
    miel_types = MielType.objects.all()
    consommable_types = ConsommableType.objects.select_related('unite').all()
    unite_mesures = UniteMesure.objects.all()
    
    return render(request, "commerce/miels/form.html", {
        "miel_types": miel_types,
        "consommable_types": consommable_types,
        "unite_mesures": unite_mesures
    })

def commande_form(request):
    from projet.models.productions import Miel
    
    if request.method == "POST":
        # Handle form submission
        client_id = request.POST.get('client')
        livraison_date = request.POST.get('livraison_date')
        note = request.POST.get('note', '')
        
        # Get client
        try:
            client = Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            return redirect('commande_form')
        
        # Create commande
        commande = Commande.objects.create(
            client=client,
            livraison_date=livraison_date,
            note=note,
            vente=None  # No vente initially
        )
        
        # Process cart items
        cart_items = request.POST.getlist('cart_items')
        for item in cart_items:
            if item:  # Skip empty items
                miel_id, quantite = item.split('|')
                try:
                    miel = Miel.objects.get(id=miel_id)
                    from projet.models.ventes import CommandeDetail
                    CommandeDetail.objects.create(
                        commande=commande,
                        miel=miel,
                        quantite=int(quantite)
                    )
                except (Miel.DoesNotExist, ValueError):
                    continue
        
        # Create initial status
        try:
            initial_status = CommandeStatus.objects.get(name='Créée')
            from projet.models.ventes import CommandeStatusHistory
            CommandeStatusHistory.objects.create(
                commande=commande,
                commande_status=initial_status
            )
        except CommandeStatus.DoesNotExist:
            pass
        
        return redirect('commandes_list')
    
    # GET request - show form
    clients = Client.objects.all().values('id', 'name')
    miels = Miel.objects.select_related('miel_type', 'consommable_type', 'unite_mesure').all()
    
    miels_data = []
    for miel in miels:
        # Get latest price
        latest_price = miel.miel_price_histories.order_by('-created_at').first()
        price = latest_price.price if latest_price else 0.0
        
        miels_data.append({
            'id': miel.id,
            'nom': f"{miel.miel_type.name} - {miel.consommable_type.name}",
            'prix': price,
            'unite': miel.unite_mesure.name,
            'quantite_unite': miel.quantite_unite
        })
    
    return render(request, "commerce/commandes/form.html", {
        "clients": clients,
        "miels": miels_data
    })

def miel_stats(request):
    from projet.models.productions import Miel, MielStock, MielPriceHistory
    from django.db.models import Sum, Count, F, Q
    from django.db.models.functions import TruncDate
    from datetime import datetime, timedelta
    from collections import defaultdict
    import json
    
    # Get selected date or use today
    selected_date = request.GET.get('date', datetime.now().strftime('%Y-%m-%d'))
    filter_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
    
    # Get all miels with related data
    miels = Miel.objects.select_related(
        'miel_type', 'consommable_type', 'unite_mesure'
    ).prefetch_related(
        'miel_stock', 'miel_price_histories'
    ).all()
    
    stats = []
    
    for miel in miels:
        # Calculate stock at selected date
        stock_entries = miel.miel_stock.filter(created_at__date__lte=filter_date)
        stock_actuel = stock_entries.aggregate(total=Sum('added_quantity'))['total'] or 0
        
        # Calculate initial stock (first entry)
        first_entry = miel.miel_stock.order_by('created_at').first()
        stock_initial = first_entry.added_quantity if first_entry else 0
        
        # Calculate total entries and exits
        total_entrees = stock_entries.filter(added_quantity__gt=0).aggregate(
            total=Sum('added_quantity'))['total'] or 0
        nb_entrees = stock_entries.filter(added_quantity__gt=0).count()
        
        total_sorties = abs(stock_entries.filter(added_quantity__lt=0).aggregate(
            total=Sum('added_quantity'))['total'] or 0)
        nb_sorties = stock_entries.filter(added_quantity__lt=0).count()
        
        # Get latest price up to selected date
        latest_price_entry = miel.miel_price_histories.filter(
            created_at__date__lte=filter_date
        ).order_by('-created_at').first()
        prix_unitaire = latest_price_entry.price if latest_price_entry else 0.0
        
        # Calculate stock value
        valeur_stock = stock_actuel * prix_unitaire
        
        # Calculate stock evolution over time (last 30 days)
        start_date = filter_date - timedelta(days=30)
        daily_stock = defaultdict(int)
        
        # Get cumulative stock for each day
        for entry in miel.miel_stock.filter(
            created_at__date__gte=start_date,
            created_at__date__lte=filter_date
        ).order_by('created_at'):
            date_str = entry.created_at.strftime('%Y-%m-%d')
            daily_stock[date_str] += entry.added_quantity
        
        # Convert to cumulative values
        evolution_stock = []
        evolution_dates = []
        running_total = stock_initial
        
        current_date = start_date
        while current_date <= filter_date:
            date_str = current_date.strftime('%Y-%m-%d')
            if date_str in daily_stock:
                running_total += daily_stock[date_str]
            evolution_dates.append(date_str)
            evolution_stock.append(running_total)
            current_date += timedelta(days=1)
        
        stats.append({
            'type': miel.miel_type.name,
            'stock_actuel': stock_actuel,
            'stock_initial': stock_initial,
            'total_entrees': total_entrees,
            'nb_entrees': nb_entrees,
            'total_sorties': total_sorties,
            'nb_sorties': nb_sorties,
            'valeur_stock': valeur_stock,
            'prix_unitaire': prix_unitaire,
            'evolution_stock': json.dumps(evolution_stock),
            'evolution_dates': json.dumps(evolution_dates)
        })
    
    return render(request, 'commerce/miels/stats.html', {
        'stats': stats,
        'selected_date': selected_date
    })

def ventes_stats(request):
    from projet.models.ventes import Vente, VenteDetail
    from projet.models.productions import Miel, MielType
    from django.db.models import Sum, Count, F, Q
    from django.db.models.functions import TruncDate
    from collections import defaultdict
    import json
    
    # Get all vente details with related data
    vente_details = VenteDetail.objects.select_related(
        'miel__miel_type', 'miel__consommable_type', 'vente__mode_payement'
    ).all()
    
    # Group by miel type
    stats_by_type = defaultdict(lambda: {
        'total_quantite': 0,
        'total_montant': 0.0,
        'nb_ventes': 0,
        'ventes_evolution_dates': [],
        'ventes_evolution_qte': [],
        'ventes_par_mode': defaultdict(int)
    })
    
    # Calculate statistics for each miel type
    for detail in vente_details:
        miel_type = detail.miel.miel_type.name
        prix_unitaire = detail.miel.prix_unitaire
        montant = detail.quantite * prix_unitaire
        
        stats_by_type[miel_type]['total_quantite'] += detail.quantite
        stats_by_type[miel_type]['total_montant'] += montant
        stats_by_type[miel_type]['nb_ventes'] += 1
        
        # Count by payment mode
        mode_payement = detail.vente.mode_payement.name
        stats_by_type[miel_type]['ventes_par_mode'][mode_payement] += 1
    
    # Calculate evolution data for each type
    for miel_type in stats_by_type.keys():
        # Get daily sales evolution for this miel type
        daily_sales = VenteDetail.objects.filter(
            miel__miel_type__name=miel_type
        ).annotate(
            date=TruncDate('vente__created_at')
        ).values('date').annotate(
            total_quantite=Sum('quantite')
        ).order_by('date')
        
        dates = []
        quantities = []
        for sale in daily_sales:
            dates.append(sale['date'].strftime('%Y-%m-%d'))
            quantities.append(sale['total_quantite'])
        
        stats_by_type[miel_type]['ventes_evolution_dates'] = dates
        stats_by_type[miel_type]['ventes_evolution_qte'] = quantities
    
    # Format data for template
    stats = []
    for miel_type, data in stats_by_type.items():
        stats.append({
            'type': miel_type,
            'total_quantite': data['total_quantite'],
            'total_montant': data['total_montant'],
            'nb_ventes': data['nb_ventes'],
            'ventes_evolution_dates': json.dumps(data['ventes_evolution_dates']),
            'ventes_evolution_qte': json.dumps(data['ventes_evolution_qte']),
            'ventes_par_mode': json.dumps(dict(data['ventes_par_mode']))
        })
    
    return render(request, 'commerce/ventes/stats.html', {
        'stats': stats
    })