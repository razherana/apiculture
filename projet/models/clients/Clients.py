from django.db import models

class ClientType(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'client_types'
        
class Client(models.Model):
    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    email = models.EmailField()
    note = models.TextField()
    adresse = models.CharField(max_length=255)
    client_type_id = models.ForeignKey(ClientType, on_delete=models.CASCADE,related_name='clients')
    
    class Meta:
        db_table = 'clients'
    