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
        
class RucheHausseHistory(models.Model):
    ruche_id = models.ForeignKey(Ruche, on_delete=models.CASCADE,related_name='ruche_hausse_histories')
    hausse_id = models.ForeignKey(Hausse, on_delete=models.CASCADE,related_name='ruche_hausse_histories')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'ruche_hausse_histories'
        


class CadreType(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'cadre_types'
        
class HausseType(model.Model):
    name = models.CharField(max_length=255)
    cadre_max_capacity = models.IntegerField() #mbola tsy aiko tsara ny type-ny
    cadre_type_id = models.ForeignKey(CadreType, on_delete=models.CASCADE,related_name='hausse_types')
    
    class Meta:
        db_table = 'hausse_types'
    
class Hausse(models.Model):
    hausse_type_id = models.ForeignKey(HausseType, on_delete=models.CASCADE,related_name='hausses')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'hausses'
        
class HausseCadre(models.Model):
    hausse_id = models.ForeignKey(Hausse, on_delete=models.CASCADE,related_name='hausse_cadres')
    added_cadre = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'hausse_cadres'
        

class LocalizationStatus(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'localization_status'
        
class Localization(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_lenght=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'localizations'
        
class LocalizationStatusHistory(models.Model):
    localization_id = models.ForeignKey(Localization, on_delete=models.CASCADE,related_name='localization_status_histories')
    localization_status_id = models.ForeignKey(LocalizationStatus, on_delete=models.CASCADE,related_name='localization_status_histories')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'localization_status_histories'
        

    
    
        
