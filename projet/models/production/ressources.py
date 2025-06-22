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
        
class Materiel(models.Model):
    durre_de_vie_estimee = models.IntegerField()
    materiel_type_id = models.ForeignKey(MaterielType, on_delete=models.CASCADE,related_name='materiels')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'materiels'
        
class MaterielType(models.Model):
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    seuil_alerte = models.IntegerField()
    
    class Meta:
        db_table = 'materiel_types'
        
class MaterielStatus(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'materiel_status'
        
class MaterielStatusHistory(models.Model):
    materiel_id = models.ForeignKey(Materiel, on_delete=models.CASCADE,related_name='materiel_status_histories')
    materiel_status_id = models.ForeignKey(MaterielStatus, on_delete=models.CASCADE,related_name='materiel_status_histories')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'materiel_status_histories'