from django.db import models

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