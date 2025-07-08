from django.shortcuts import redirect, render
from django.contrib import messages

from projet.models.ventes import Client, ClientType, Commande, CommandeStatus


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
        if cmd['statut'] in ['En attente', 'Créée', 'En préparation']
    ]

    commandes_livrees = [
        cmd for cmd in commandes_data 
        if cmd['statut'] in ['Livrée', 'Terminée']
    ]

    return render(request, "commerce/commandes/list.html", {
        "commandes_en_attente": commandes_en_attente,
        "commandes_livrees": commandes_livrees,
    })


def ventes_list(request):
    ventes = [
        {'id': 1, 'date': '2025-06-18', 'client': 'Dupont',
            'produit': 'Miel de fleurs', 'quantite': 2, 'montant': 17.0},
        {'id': 2, 'date': '2025-06-17', 'client': 'Martin',
            'produit': 'Miel d’acacia', 'quantite': 1, 'montant': 10.0},
    ]
    return render(request, "commerce/ventes/list.html", {"ventes": ventes})


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
    vente = {
        'id': 1,
        'miel': 'Miel de fleurs',
        'client': 'Dupont Jean',
        'mode_payement': 'Carte bancaire',
        'note': 'Livraison rapide',
        'date': '2025-06-18',
        'quantite': 2,
        'montant': 17.0,
    }
    modes_payement = [
        {'id': 1, 'mode': 'Carte bancaire'},
        {'id': 2, 'mode': 'Chèque'},
        {'id': 3, 'mode': 'Espèces'},
    ]
    clients = [
        {'id': 1, 'nom': 'Dupont Jean'},
        {'id': 2, 'nom': 'Martin Paul'},
    ]
    miels = [
        {'id': 1, 'nom': 'Miel de fleurs'},
        {'id': 2, 'nom': 'Miel d’acacia'},
    ]
    return render(request, "commerce/ventes/vue.html", {
        "vente": vente,
        "modes_payement": modes_payement,
        "clients": clients,
        "miels": miels
    })


def vente_form(request):
    modes_payement = [
        {'id': 1, 'mode': 'Carte bancaire'},
        {'id': 2, 'mode': 'Chèque'},
        {'id': 3, 'mode': 'Espèces'},
    ]
    clients = [
        {'id': 1, 'nom': 'Dupont Jean'},
        {'id': 2, 'nom': 'Martin Paul'},
    ]
    miels = [
        {'id': 1, 'nom': 'Miel de fleurs'},
        {'id': 2, 'nom': 'Miel d’acacia'},
    ]
    return render(request, "commerce/ventes/form.html", {
        "modes_payement": modes_payement,
        "clients": clients,
        "miels": miels
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


def miels_stats(request):
    from projet.models.productions import Miel, MielStock, MielPriceHistory
    from django.db.models import Sum, Count
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
    
    stats = []
    for miel in miels_queryset:
        # Calculate stock at selected date
        stock_entries = miel.miel_stock.filter(created_at__date__lte=filter_date)
        stock_actuel = stock_entries.aggregate(total=Sum('added_quantity'))['total'] or 0
        
        # Calculate initial stock (from beginning of year)
        year_start = date(filter_date.year, 1, 1)
        initial_stock_entries = miel.miel_stock.filter(created_at__date__lt=year_start)
        stock_initial = initial_stock_entries.aggregate(total=Sum('added_quantity'))['total'] or 0
        
        # Calculate entries and exits for the year up to selected date
        year_entries = miel.miel_stock.filter(
            created_at__date__range=[year_start, filter_date],
            added_quantity__gt=0
        )
        year_exits = miel.miel_stock.filter(
            created_at__date__range=[year_start, filter_date],
            added_quantity__lt=0
        )
        
        total_entrees = year_entries.aggregate(total=Sum('added_quantity'))['total'] or 0
        total_sorties = abs(year_exits.aggregate(total=Sum('added_quantity'))['total'] or 0)
        nb_entrees = year_entries.count()
        nb_sorties = year_exits.count()
        
        # Get current price at selected date
        latest_price_entry = miel.miel_price_histories.filter(
            created_at__date__lte=filter_date
        ).order_by('-created_at').first()
        prix_unitaire = latest_price_entry.price if latest_price_entry else 0.0
        
        # Calculate stock value
        valeur_stock = stock_actuel * prix_unitaire
        
        # Generate evolution data (last 6 months from selected date)
        evolution_stock = []
        evolution_dates = []
        
        for i in range(5, -1, -1):
            # Calculate date i months before selected date
            month = filter_date.month - i
            year = filter_date.year
            while month <= 0:
                month += 12
                year -= 1
            
            try:
                evolution_date = date(year, month, min(filter_date.day, 28))
            except ValueError:
                evolution_date = date(year, month, 28)
            
            # Calculate stock at that date
            historical_entries = miel.miel_stock.filter(created_at__date__lte=evolution_date)
            historical_stock = historical_entries.aggregate(total=Sum('added_quantity'))['total'] or 0
            
            evolution_stock.append(historical_stock)
            evolution_dates.append(evolution_date.strftime('%Y-%m-%d'))
        
        miel_stats = {
            "type": miel.miel_type.name,
            "stock_actuel": stock_actuel,
            "stock_initial": stock_initial,
            "total_entrees": total_entrees,
            "total_sorties": total_sorties,
            "nb_entrees": nb_entrees,
            "nb_sorties": nb_sorties,
            "valeur_stock": valeur_stock,
            "prix_unitaire": prix_unitaire,
            "evolution_stock": evolution_stock,
            "evolution_dates": evolution_dates
        }
        stats.append(miel_stats)
    
    return render(request, "commerce/miels/stats.html", {
        "stats": stats,
        "selected_date": selected_date
    })


def ventes_stats(request):
    stats = [
        {
            "type": "Fleurs",
            "total_quantite": 25,
            "total_montant": 220.0,
            "nb_ventes": 12,
            "ventes_evolution_dates": ["2025-01-01", "2025-02-01", "2025-03-01", "2025-04-01", "2025-05-01", "2025-06-01"],
            "ventes_evolution_qte": [2, 5, 7, 4, 3, 4],
            "ventes_par_mode": {
                "Carte bancaire": 8,
                "Chèque": 2,
                "Espèces": 2
            }
        },
        {
            "type": "Acacia",
            "total_quantite": 15,
            "total_montant": 170.0,
            "nb_ventes": 7,
            "ventes_evolution_dates": ["2025-01-01", "2025-02-01", "2025-03-01", "2025-04-01", "2025-05-01", "2025-06-01"],
            "ventes_evolution_qte": [0, 1, 3, 4, 5, 2],
            "ventes_par_mode": {
                "Carte bancaire": 3,
                "Chèque": 1,
                "Espèces": 3
            }
        }
    ]
    return render(request, "commerce/ventes/stats.html", {"stats": stats})


def commandes_stats(request):
    stats_par_type = {
        "Fleurs": {
            "total_commandes": 57,
            "commandes_livrees": 50,
            "commandes_annulees": 4,
            "taux_livraison": 50 / 57,
            "ca_estime": 1250.0,
            "repartition_par_jour": {
                "2025-06-01": 5,
                "2025-06-02": 7,
                "2025-06-03": 6,
                "2025-06-04": 4,
                "2025-06-05": 8,
                "2025-06-06": 10,
                "2025-06-07": 17
            },
            "top_clients": ["Durand", "Petit", "Lemoine"]
        },
        "Acacia": {
            "total_commandes": 34,
            "commandes_livrees": 29,
            "commandes_annulees": 2,
            "taux_livraison": 29 / 34,
            "ca_estime": 1020.0,
            "repartition_par_jour": {
                "2025-06-01": 4,
                "2025-06-02": 3,
                "2025-06-03": 5,
                "2025-06-04": 6,
                "2025-06-06": 8,
                "2025-06-07": 8
            },
            "top_clients": ["Bernard", "Martin", "Durand"]
        },
        "Châtaignier": {
            "total_commandes": 20,
            "commandes_livrees": 15,
            "commandes_annulees": 3,
            "taux_livraison": 15 / 20,
            "ca_estime": 700.0,
            "repartition_par_jour": {
                "2025-06-01": 2,
                "2025-06-03": 4,
                "2025-06-05": 5,
                "2025-06-06": 5,
                "2025-06-07": 4
            },
            "top_clients": ["Petit", "Thomas", "Bernard"]
        }
    }

    stats_globales = {
        "total_commandes": 111,
        "commandes_livrees": 94,
        "commandes_annulees": 9,
        "taux_livraison": 94 / 111,
        "ca_estime": 1250.0 + 1020.0 + 700.0,
        "produit_plus_vendu": "Fleurs",
        "client_fidele": "Durand",
        "courbe_jour_labels": ["2025-06-01", "2025-06-02", "2025-06-03", "2025-06-04", "2025-06-05", "2025-06-06", "2025-06-07"],
        "courbe_jour_valeurs": [11, 10, 15, 10, 13, 23, 29]
    }

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
    
    return render(request, "commerce/miels/form.html", {
        "miel_types": miel_types,
        "consommable_types": consommable_types,
        "unite_mesures": unite_mesures
    })
