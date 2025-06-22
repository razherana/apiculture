from django.db import models 

class RucheStatus(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'ruche_status'
        
class RucheType(models.Model):
    name = models.CharField(max_length=255)
    hausse_max_capacity = models.IntegerField()
    hausses_type_id = models.ForeignKey(HausseType, on_delete=models.CASCADE,related_name='ruche_types')
    
    class Meta:
        db_table = 'ruches_types'
        
class Ruche(models.Model):
    description = models.CharField(max_length=255)
    localizations_id = models.ForeignKey(Localization, on_delete=models.CASCADE,related_name='ruches')
    ruche_type_id = models.ForeignKey(RucheType, on_delete=models.CASCADE,related_name='ruches')
    essaim_id = models.ForeignKey(Essaim, on_delete=models.CASCADE,related_name='ruches')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'ruches'
        
class RucheStatusHistory(models.Model):
    ruche_id = models.ForeignKey(Ruche, on_delete=models.CASCADE,related_name='ruche_status_histories')
    ruche_status_id = models.ForeignKey(RucheStatus, on_delete=models.CASCADE,related_name='ruche_status_histories')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'ruche_status_histories'
        
