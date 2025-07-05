from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from projet.models.ressources import UniteMesure, ConsommableType, Ruche, Localization


# Honey (Miel) Models
class MielType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'miel_types'


class Miel(models.Model):
    consommable_type_id = models.ForeignKey(
        ConsommableType, on_delete=models.CASCADE, related_name='miels')
    unite_mesure_id = models.ForeignKey(
        UniteMesure, on_delete=models.CASCADE, related_name='miels')
    quantite_unite = models.IntegerField()
    miel_type_id = models.ForeignKey(
        MielType, on_delete=models.CASCADE, related_name='miels')

    class Meta:
        db_table = 'miels'


class MielPriceHistory(models.Model):
    miel_id = models.ForeignKey(
        Miel, on_delete=models.CASCADE, related_name='miel_price_histories')
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'miel_price_histories'


class MielStock(models.Model):
    miel_id = models.ForeignKey(
        Miel, on_delete=models.CASCADE, related_name='miel_stock')
    added_quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'miel_stock'


# Calendar and Task Models
class InterventionType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'intervention_type'


class Intervention(models.Model):
    title = models.CharField(max_length=255)
    donnees = models.TextField()
    ruche_id = models.ForeignKey(
        Ruche, on_delete=models.CASCADE, related_name='intervention')
    localization_id = models.ForeignKey(
        Localization, on_delete=models.CASCADE, related_name='intervention')
    intervention_type_id = models.ForeignKey(
        InterventionType, on_delete=models.CASCADE, related_name='intervention')
    details = models.CharField(max_length=255)
    date_prevue = models.DateField()
    date_realisation = models.DateField()

    class Meta:
        db_table = 'intervention'


class TaskType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'task_types'


class TaskPriorite(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'task_priorites'


class TaskStatusType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'task_status_type'


class Task(models.Model):
    title = models.CharField(max_length=255)
    ruche_id = models.ForeignKey(
        Ruche, on_delete=models.CASCADE, related_name='tasks')
    localization_id = models.ForeignKey(
        Localization, on_delete=models.CASCADE, related_name='tasks')
    task_type_id = models.ForeignKey(
        TaskType, on_delete=models.CASCADE, related_name='tasks')
    description = models.CharField(max_length=255)
    task_priorite_id = models.ForeignKey(
        TaskPriorite, on_delete=models.CASCADE, related_name='tasks')
    date_prevue = models.DateField()
    date_realisation = models.DateField()

    class Meta:
        db_table = 'tasks'


class TaskStatusHistory(models.Model):
    task_id = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='task_status_histories')
    task_status_type_id = models.ForeignKey(
        TaskStatusType, on_delete=models.CASCADE, related_name='task_status_histories')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'task_status_histories'


class Recolte(models.Model):
    ruche = models.ForeignKey(
        Ruche, on_delete=models.CASCADE, related_name='recoltes')
    poids_miel = models.FloatField()
    taux_humidite = models.FloatField()
    qualite = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'recoltes'
