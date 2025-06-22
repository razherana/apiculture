from django.db import models 

class InterventionType(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'intervention_type'
        
class Intervention(models.Model):
    title = models.CharField(max_length=255)
    donnees = models.TextField()
    ruche_id = models.ForeignKey(Ruche, on_delete=models.CASCADE,related_name='intervention')
    localization_id = models.ForeignKey(Localization, on_delete=models.CASCADE,related_name='intervention')
    intervention_type_id = models.ForeignKey(InterventionType, on_delete=models.CASCADE,related_name='intervention')
    details = models.CharField(max_length=255) 
    date_prevue = models.DateField()
    date_realisation = models.DateField()
    
    class Meta:
        db_table = 'intervention'

