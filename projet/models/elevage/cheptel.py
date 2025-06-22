from django.db import models 

class EssaimOrigin(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'essaim_origins'
        
class EssaimRace(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'essaim_races'
        
class Essaim(models.Model):
    essaim_origin_id = models.ForeignKey(EssaimOrigin, on_delete=models.CASCADE,related_name='essaims')
    essaim_race_id = models.ForeignKey(EssaimRace, on_delete=models.CASCADE,related_name='essaims')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'essaims'
        
class EssaimStatus(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'essaim_status'

class EssaimStatusHistory(models.Model):
    issaim_id = models.ForeignKey(Essaim, on_delete=models.CASCADE,related_name='essaim_status_histories')
    issaim_status_id = models.ForeignKey(EssaimStatus, on_delete=models.CASCADE,related_name='essaim_status_histories')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'essaim_status_histories'
        
class EssaimDetail(models.Model):
    note = models.TextField()
    is_death = is_admin = models.BooleanField()
    issaim_id = models.ForeignKey(Essaim, on_delete=models.CASCADE,related_name='essaim_details')
    ouvrier_added = models.IntegerField() #tsy aiko ny type
    faux_bourdon_added = models.IntegerField() #tsy aiko ny type
    reine_added = models.IntegerField() #tsy aiko ny type
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'essaim_details'
        
class Comportement(models.Model):
    description = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'comportements'
        
class EssaimSanteHistory(models.Model):
    issaim_id = models.ForeignKey(Essaim, on_delete=models.CASCADE,related_name='essaim_sante_histories')
    force_colonie = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(10)])
    comportement_id = models.ForeignKey(Comportement, on_delete=models.CASCADE,related_name='essaim_sante_histories')
    egg_present = models.BooleanField()
    couvain_present = models.BooleanField()
    reine_present = models.BooleanField()
    parasite = models.CharField(max_length=255)
    maladie = models.CharField(max_length=255)
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'essaim_sante_histories'
    
    