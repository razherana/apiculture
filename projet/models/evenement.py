from django.db import models
from django.conf import settings

class Evenement(models.Model):
    titre = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date = models.DateField()
    heure = models.TimeField(null=True, blank=True)
    ruche = models.ForeignKey('projet.Ruche', null=True, blank=True, on_delete=models.SET_NULL, related_name='evenements')
    localisation = models.ForeignKey('projet.Localization', null=True, blank=True, on_delete=models.SET_NULL, related_name='evenements')
    type = models.CharField(max_length=100, choices=[
        ('inspection', 'Inspection'),
        ('treatment', 'Traitement'),
        ('task', 'Tâche'),
        ('urgent', 'Urgent'),
        ('harvest', 'Récolte'),
        ('autre', 'Autre'),
    ], default='autre')
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Événement"
        verbose_name_plural = "Événements"
        ordering = ['-date', '-heure']

    def __str__(self):
        return f"{self.titre} ({self.date})"
