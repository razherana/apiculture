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
    unite = models.ForeignKey(
        UniteMesure, on_delete=models.CASCADE, related_name='consommable_types')
    seuil_alerte = models.IntegerField()

    class Meta:
        db_table = 'consommable_types'


class Consommable(models.Model):
    consommable_type = models.ForeignKey(
        ConsommableType, on_delete=models.CASCADE, related_name='consommables')
    date_de_peremption = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'consommables'


class ConsommableConsomme(models.Model):
    consommable = models.ForeignKey(
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
    materiel_type = models.ForeignKey(
        MaterielType, on_delete=models.CASCADE, related_name='materiels')
    created_at = models.DateTimeField(auto_now_add=True)
    nb = models.IntegerField(default=1)  # Ajout du champ nombre

    class Meta:
        db_table = 'materiels'


class MaterielStatus(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'materiel_status'


class MaterielStatusHistory(models.Model):
    materiel = models.ForeignKey(
        Materiel, on_delete=models.CASCADE, related_name='materiel_status_histories')
    materiel_status = models.ForeignKey(
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
    description = models.CharField(max_length=255, blank=True, null=True)
    essaim_origin = models.ForeignKey(
        EssaimOrigin, on_delete=models.CASCADE, related_name='essaims')
    essaim_race = models.ForeignKey(
        EssaimRace, on_delete=models.CASCADE, related_name='essaims')
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def population(self):
        total_population = {
            'ouvriers': 0,
            'faux_bourdons': 0,
            'reines': 0,
            'total': 0
        }
        
        population_details = self.essaim_details.all().order_by('-created_at')
        
        for detail in population_details:
            if detail.is_death:
                total_population['ouvriers'] -= abs(detail.ouvrier_added)
                total_population['faux_bourdons'] -= abs(detail.faux_bourdon_added)
                total_population['reines'] -= abs(detail.reine_added)
            else:
                total_population['ouvriers'] += detail.ouvrier_added
                total_population['faux_bourdons'] += detail.faux_bourdon_added
                total_population['reines'] += detail.reine_added
        
        return total_population
    class Meta:
        db_table = 'essaims'


class EssaimStatus(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'essaim_status'


class EssaimStatusHistory(models.Model):
    essaim = models.ForeignKey(
        Essaim, on_delete=models.CASCADE, related_name='essaim_status_histories')
    essaim_status = models.ForeignKey(
        EssaimStatus, on_delete=models.CASCADE, related_name='essaim_status_histories')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'essaim_status_histories'


class EssaimDetail(models.Model):
    note = models.TextField()
    is_death = models.BooleanField()
    essaim = models.ForeignKey(
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
    essaim = models.ForeignKey(
        Essaim, on_delete=models.CASCADE, related_name='essaim_sante_histories')
    force_colonie = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)])
    comportement = models.ForeignKey(
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
    cadre_type = models.ForeignKey(
        CadreType, on_delete=models.CASCADE, related_name='hausse_types')

    class Meta:
        db_table = 'hausse_types'


class RucheType(models.Model):
    name = models.CharField(max_length=255)
    hausse_max_capacity = models.IntegerField()
    hausses_type = models.ForeignKey(
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
    localization = models.ForeignKey(
        Localization, on_delete=models.CASCADE, related_name='localization_status_histories')
    localization_status = models.ForeignKey(
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
    localizations = models.ForeignKey(
        Localization, on_delete=models.CASCADE, related_name='ruches')
    ruche_type = models.ForeignKey(
        RucheType, on_delete=models.CASCADE, related_name='ruches')
    essaim = models.ForeignKey(
        Essaim, on_delete=models.CASCADE, related_name='ruches', null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ruches'


class RucheStatusHistory(models.Model):
    ruche = models.ForeignKey(
        Ruche, on_delete=models.CASCADE, related_name='ruche_status_histories')
    ruche_status = models.ForeignKey(
        RucheStatus, on_delete=models.CASCADE, related_name='ruche_status_histories')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ruche_status_histories'


class Hausse(models.Model):
    hausse_type = models.ForeignKey(
        HausseType, on_delete=models.CASCADE, related_name='hausses')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hausses'


class HausseCadre(models.Model):
    hausse = models.ForeignKey(
        Hausse, on_delete=models.CASCADE, related_name='hausse_cadres')
    added_cadre = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hausse_cadres'


class RucheHausseHistory(models.Model):
    ruche = models.ForeignKey(
        Ruche, on_delete=models.CASCADE, related_name='ruche_hausse_histories')
    hausse = models.ForeignKey(
        Hausse, on_delete=models.CASCADE, related_name='ruche_hausse_histories')
    created_at = models.DateTimeField(auto_now_add=True)
    is_removed = models.BooleanField(default=False)

    class Meta:
        db_table = 'ruche_hausse_histories'


class PrixMateriel(models.Model):
    materiel = models.ForeignKey(
        Materiel, on_delete=models.CASCADE, related_name='prix_materiels'
    )
    prix_materiel = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'prix_materiel'
