from django.db import models

class Recolte(models.Model):
    ruche_id = models.ForeignKey(Ruche, on_delete=models.CASCADE,related_name='recoltes')
    poids_miel = models.FloatField()
    taux_humidite = models.FloatField()
    quantite = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(10)])
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'recoltes'
