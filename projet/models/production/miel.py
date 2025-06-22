from django.db import models 

class MielType(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'miel_types'
        
class UniteMesure(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'unite_mesures'
        
class Miel(models.Model):
    consommable_type_id = models.ForeignKey(ConsommableType, on_delete=models.CASCADE,related_name='miels')
    unite_mesure_id = models.ForeignKey(UniteMesure, on_delete=models.CASCADE,related_name='miels')
    quantite_unite = models.IntegerField() #tsy hay ny type_ny
    miel_type_id = models.ForeignKey(MielType, on_delete=models.CASCADE,related_name='miels')
    
    class Meta:
        db_table = 'miels'
        

        
class MielPriceHistory(models.Model):
    miel_id = models.ForeignKey(Miel, on_delete=models.CASCADE,related_name='miel_price_histories')
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'miel_price_histories'
        