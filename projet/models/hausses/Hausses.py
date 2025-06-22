from django.db import models 

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
        
class RucheHausseHistory(models.Model):
    ruche_id = models.ForeignKey(Ruche, on_delete=models.CASCADE,related_name='ruche_hausse_histories')
    hausse_id = models.ForeignKey(Hausse, on_delete=models.CASCADE,related_name='ruche_hausse_histories')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'ruche_hausse_histories'
    
    