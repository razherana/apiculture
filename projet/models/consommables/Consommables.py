from django.db import models 

class ConsommableType(models.Model):
    name = models.CharField(max_length=255)
    unite_id = models.ForeignKey(UniteMesure, on_delete=models.CASCADE,related_name='consommable_types')
    seuil_alerte = models.IntegerField()
    
    
    class Meta:
        db_table = 'consommable_types'
        
class Consommable(models.Model):
    consommable_type_id = models.ForeignKey(ConsommableType, on_delete=models.CASCADE,related_name='consommables')
    date_de_peremption = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'consommables'
        
class ConsommableConsomme(models.Model):
    consommable_id = models.ForeignKey(Consommable, on_delete=models.CASCADE,related_name='consommable_consomme')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'consommable_consomme'