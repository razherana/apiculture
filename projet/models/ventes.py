from django.db import models

from projet.models.productions import Miel


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
    client_type = models.ForeignKey(
        ClientType, on_delete=models.CASCADE, related_name='clients')

    @property
    def get_last_commande(self) -> str:
        last_commande = self.commandes.order_by('-created_at').first()
        last_vente = self.ventes.order_by('-created_at').first()
        if last_vente and last_commande:
            return max(last_vente.created_at, last_commande.created_at)
        elif last_vente:
            return last_vente.created_at
        elif last_commande:
            return last_commande.created_at
        return '-'

    class Meta:
        db_table = 'clients'


class CommandeStatus(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'commande_status'


class ModePayement(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'mode_payements'


class Vente(models.Model):
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name='ventes')
    mode_payement = models.ForeignKey(
        ModePayement, on_delete=models.CASCADE, related_name='ventes')
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ventes'


class VenteDetail(models.Model):
    miel = models.ForeignKey(
        Miel, on_delete=models.CASCADE, related_name='vente_details')
    vente = models.ForeignKey(
        Vente, on_delete=models.CASCADE, related_name='vente_details')
    quantite = models.IntegerField()

    class Meta:
        db_table = 'vente_details'


class Commande(models.Model):
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name='commandes')
    vente = models.ForeignKey(
        Vente, on_delete=models.CASCADE, related_name='commande', null=True)
    note = models.TextField()
    livraison_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'commandes'


class CommandeDetail(models.Model):
    miel = models.ForeignKey(
        Miel, on_delete=models.CASCADE, related_name='commande_details')
    commande = models.ForeignKey(
        Commande, on_delete=models.CASCADE, related_name='commande_details')
    quantite = models.IntegerField()

    class Meta:
        db_table = 'commande_details'


class CommandeStatusHistory(models.Model):
    commande = models.ForeignKey(
        Commande, on_delete=models.CASCADE, related_name='commande_status_histories')
    commande_status = models.ForeignKey(
        CommandeStatus, on_delete=models.CASCADE, related_name='commande_status_histories')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'commande_status_histories'
