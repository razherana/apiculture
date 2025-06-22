from django.db import models 

class MielStock(models.Model):
    miel_id = models.ForeignKey(Miel, on_delete=models.CASCADE,related_name='miel_stock')
    added_quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'miel_stock'
