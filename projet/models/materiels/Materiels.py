from django.db import models 

class Materiel(models.Model):
    durre_de_vie_estimee = models.IntegerField()
    materiel_typeiid = models.ForeignKey(MaterielType, on_delete=models.CASCADE,related_name='materiels')
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
        
        
        
    