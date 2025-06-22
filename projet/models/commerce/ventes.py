from django.db import models 

class CommandeStatus(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'commande_status'
        
class ModePayement(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'mode_payements'
        
class Vente(models.Model):
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE,related_name='ventes')
    mode_payement_id = models.ForeignKey(ModePayement, on_delete=models.CASCADE,related_name='ventes')
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'ventes'
        
class VenteDetail(models.Model):
    miel_id = models.ForeignKey(Miel, on_delete=models.CASCADE,related_name='vente_details')
    vente_id = models.ForeignKey(Vente, on_delete=models.CASCADE,related_name='vente_details')
    quantite = models.IntegerField()
    
    class Meta:
        db_table = 'vente_details'
        
class Commande(models.Model):
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE,related_name='commandes')
    vente_id = models.ForeignKey(Vente, on_delete=models.CASCADE,related_name='commandes')
    note = models.TextField()
    livraison_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'commandes'
        
class CommandeDetail(models.Model):
    miel_id = models.ForeignKey(Miel, on_delete=models.CASCADE,related_name='commande_details')
    commande_id = models.ForeignKey(Commande, on_delete=models.CASCADE,related_name='commande_details')
    quantite = models.IntegerField()
    
    class Meta:
        db_table = 'commande_details'
        
class CommandeStatusHistory(models.Model):
    commande_id = models.ForeignKey(Commande, on_delete=models.CASCADE,related_name='commande_status_histories')
    commande_status_id = models.ForeignKey(CommandeStatus, on_delete=models.CASCADE,related_name='commande_status_histories')
    
    class Meta:
        db_table = 'commande_status_histories'
        
class ClientType(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'client_types'
        
class Client(models.Model):
    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    email = models.EmailField()
    note = models.TextField()
    adresse = models.CharField(max_length=255)
    client_type_id = models.ForeignKey(ClientType, on_delete=models.CASCADE,related_name='clients')
    
    class Meta:
        db_table = 'clients'