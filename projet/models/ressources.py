from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Measurement Units
class UniteMesure(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'unite_mesures'


# Consumable Models
class ConsommableType(models.Model):
    name = models.CharField(max_length=255)
    unite_id = models.ForeignKey(
        UniteMesure, on_delete=models.CASCADE, related_name='consommable_types')
    seuil_alerte = models.IntegerField()

    class Meta:
        db_table = 'consommable_types'


class Consommable(models.Model):
    consommable_type_id = models.ForeignKey(
        ConsommableType, on_delete=models.CASCADE, related_name='consommables')
    date_de_peremption = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'consommables'


class ConsommableConsomme(models.Model):
    consommable_id = models.ForeignKey(
        Consommable, on_delete=models.CASCADE, related_name='consommable_consomme')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'consommable_consomme'


# Equipment Models
class MaterielType(models.Model):
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    seuil_alerte = models.IntegerField()

    class Meta:
        db_table = 'materiel_types'


class Materiel(models.Model):
    durre_de_vie_estimee = models.IntegerField()
    materiel_type_id = models.ForeignKey(
        MaterielType, on_delete=models.CASCADE, related_name='materiels')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'materiels'


class MaterielStatus(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'materiel_status'


class MaterielStatusHistory(models.Model):
    materiel_id = models.ForeignKey(
        Materiel, on_delete=models.CASCADE, related_name='materiel_status_histories')
    materiel_status_id = models.ForeignKey(
        MaterielStatus, on_delete=models.CASCADE, related_name='materiel_status_histories')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'materiel_status_histories'


# Swarm (Essaim) Models
class EssaimOrigin(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'essaim_origins'


class EssaimRace(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'essaim_races'


class Essaim(models.Model):
    essaim_origin_id = models.ForeignKey(
        EssaimOrigin, on_delete=models.CASCADE, related_name='essaims')
    essaim_race_id = models.ForeignKey(
        EssaimRace, on_delete=models.CASCADE, related_name='essaims')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'essaims'


class EssaimStatus(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'essaim_status'


class EssaimStatusHistory(models.Model):
    issaim_id = models.ForeignKey(
        Essaim, on_delete=models.CASCADE, related_name='essaim_status_histories')
    issaim_status_id = models.ForeignKey(
        EssaimStatus, on_delete=models.CASCADE, related_name='essaim_status_histories')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'essaim_status_histories'


class EssaimDetail(models.Model):
    note = models.TextField()
    is_death = models.BooleanField()
    essaim_id = models.ForeignKey(
        Essaim, on_delete=models.CASCADE, related_name='essaim_details')
    ouvrier_added = models.IntegerField()
    faux_bourdon_added = models.IntegerField()
    reine_added = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'essaim_details'


class Comportement(models.Model):
    description = models.CharField(max_length=255)

    class Meta:
        db_table = 'comportements'


class EssaimSanteHistory(models.Model):
    essaim_id = models.ForeignKey(
        Essaim, on_delete=models.CASCADE, related_name='essaim_sante_histories')
    force_colonie = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)])
    comportement_id = models.ForeignKey(
        Comportement, on_delete=models.CASCADE, related_name='essaim_sante_histories')
    egg_present = models.BooleanField()
    couvain_present = models.BooleanField()
    reine_present = models.BooleanField()
    parasite = models.CharField(max_length=255)
    maladie = models.CharField(max_length=255)
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'essaim_sante_histories'


# Hive (Ruche) Models
class CadreType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'cadre_types'


class HausseType(models.Model):
    name = models.CharField(max_length=255)
    cadre_max_capacity = models.IntegerField()
    cadre_type_id = models.ForeignKey(
        CadreType, on_delete=models.CASCADE, related_name='hausse_types')

    class Meta:
        db_table = 'hausse_types'


class RucheType(models.Model):
    name = models.CharField(max_length=255)
    hausse_max_capacity = models.IntegerField()
    hausses_type_id = models.ForeignKey(
        HausseType, on_delete=models.CASCADE, related_name='ruche_types')

    class Meta:
        db_table = 'ruches_types'


class LocalizationStatus(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'localization_status'


class Localization(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)  # Fixed typo in max_length
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'localizations'


class LocalizationStatusHistory(models.Model):
    localization_id = models.ForeignKey(
        Localization, on_delete=models.CASCADE, related_name='localization_status_histories')
    localization_status_id = models.ForeignKey(
        LocalizationStatus, on_delete=models.CASCADE, related_name='localization_status_histories')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'localization_status_histories'


class RucheStatus(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'ruche_status'


class Ruche(models.Model):
    description = models.CharField(max_length=255)
    localizations_id = models.ForeignKey(
        Localization, on_delete=models.CASCADE, related_name='ruches')
    ruche_type_id = models.ForeignKey(
        RucheType, on_delete=models.CASCADE, related_name='ruches')
    essaim_id = models.ForeignKey(
        Essaim, on_delete=models.CASCADE, related_name='ruches')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ruches'


class RucheStatusHistory(models.Model):
    ruche_id = models.ForeignKey(
        Ruche, on_delete=models.CASCADE, related_name='ruche_status_histories')
    ruche_status_id = models.ForeignKey(
        RucheStatus, on_delete=models.CASCADE, related_name='ruche_status_histories')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ruche_status_histories'


class Hausse(models.Model):
    hausse_type_id = models.ForeignKey(
        HausseType, on_delete=models.CASCADE, related_name='hausses')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hausses'


class HausseCadre(models.Model):
    hausse_id = models.ForeignKey(
        Hausse, on_delete=models.CASCADE, related_name='hausse_cadres')
    added_cadre = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hausse_cadres'


class RucheHausseHistory(models.Model):
    ruche_id = models.ForeignKey(
        Ruche, on_delete=models.CASCADE, related_name='ruche_hausse_histories')
    hausse_id = models.ForeignKey(
        Hausse, on_delete=models.CASCADE, related_name='ruche_hausse_histories')
    created_at = models.DateTimeField(auto_now_add=True)
    is_removed = models.BooleanField(default=False)

    class Meta:
        db_table = 'ruche_hausse_histories'
