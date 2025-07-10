from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from projet.models.ressources import (
    LocalizationStatus,
    Localization,
    CadreType,
    HausseType,
    HausseCadre,
    Hausse,
    RucheHausseHistory, 
    RucheStatus,
    Ruche,
    EssaimOrigin,
    EssaimRace,
    EssaimStatus,
    EssaimDetail,
    EssaimSanteHistory,
    Comportement,
    RucheStatusHistory, 
    RucheType,
    Essaim,
    LocalizationStatusHistory,
)

# ----------------CRUD LOCALIZATIONS STATUS--------------


def localization_status_list(request):
    statuses = LocalizationStatus.objects.all()
    return render(request, 'localization_status/list.html', {'statuses': statuses})


def localization_status_detail(request, id):
    status = get_object_or_404(LocalizationStatus, pk=id)
    return render(request, 'localization_status/detail.html', {'status': status})


def localization_status_create(request):
    if request.method == 'POST':
        name = request.POST['name']
        LocalizationStatus.objects.create(name=name)
        return redirect('localization_status_list')
    return render(request, 'localization_status/create.html')


def localization_status_update(request, id):
    status = get_object_or_404(LocalizationStatus, pk=id)
    if request.method == 'POST':
        status.name = request.POST['name']
        status.save()
        return redirect('localization_status_list')
    return render(request, 'localization_status/update.html', {'status': status})


def localization_status_delete(request, id):
    status = get_object_or_404(LocalizationStatus, pk=id)
    status.delete()
    return redirect('localization_status_list')


# ------------- CRUD LOCALIZATION ------------------

def localization_list(request):
    localizations = Localization.objects.all()
    return render(request, 'localizations/list.html', {'localizations': localizations})


def localization_detail(request, id):
    localization = get_object_or_404(Localization, pk=id)
    return render(request, 'localizations/detail.html', {'localization': localization})


def localization_create(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        Localization.objects.create(
            name=name, description=description, created_at=timezone.now())
        return redirect('localization_list')
    return render(request, 'localizations/create.html')


def localization_update(request, id):
    localization = get_object_or_404(Localization, pk=id)
    if request.method == 'POST':
        localization.name = request.POST['name']
        localization.description = request.POST['description']
        localization.save()
        return redirect('localization_list')
    return render(request, 'localizations/update.html', {'localization': localization})


def localization_delete(request, id):
    localization = get_object_or_404(Localization, pk=id)
    localization.delete()
    return redirect('localization_list')


# ----------------CRUD CADRE TYPES ------------------

def cadre_type_list(request):
    types = CadreType.objects.all()
    return render(request, 'cadre_types/list.html', {'types': types})


def cadre_type_detail(request, id):
    type = get_object_or_404(CadreType, pk=id)
    return render(request, 'cadre_types/detail.html', {'type': type})


def cadre_type_create(request):
    if request.method == 'POST':
        name = request.POST['name']
        CadreType.objects.create(name=name)
        return redirect('cadre_type_list')
    return render(request, 'cadre_types/create.html')


def cadre_type_update(request, id):
    type = get_object_or_404(CadreType, pk=id)
    if request.method == 'POST':
        type.name = request.POST['name']
        type.save()
        return redirect('cadre_type_list')
    return render(request, 'cadre_types/update.html', {'type': type})


def cadre_type_delete(request, id):
    type = get_object_or_404(CadreType, pk=id)
    type.delete()
    return redirect('cadre_type_list')


# -----------------CRUD HAUSSE TYPE -----------------

def hausse_type_list(request):
    types = HausseType.objects.select_related('cadre_type_id')
    return render(request, 'hausse_types/list.html', {'types': types})


def hausse_type_detail(request, id):
    type = get_object_or_404(HausseType, pk=id)
    return render(request, 'hausse_types/detail.html', {'type': type})


def hausse_type_create(request):
    cadre_types = CadreType.objects.all()
    if request.method == 'POST':
        name = request.POST['name']
        cadre_max_capacity = request.POST['cadre_max_capacity']
        cadre_type_id = request.POST['cadre_type_id']
        cadre_type = get_object_or_404(CadreType, pk=cadre_type_id)
        HausseType.objects.create(
            name=name, cadre_max_capacity=cadre_max_capacity, cadre_type_id=cadre_type)
        return redirect('hausse_type_list')
    return render(request, 'hausse_types/create.html', {'cadre_types': cadre_types})


def hausse_type_update(request, id):
    type = get_object_or_404(HausseType, pk=id)
    cadre_types = CadreType.objects.all()
    if request.method == 'POST':
        type.name = request.POST['name']
        type.cadre_max_capacity = request.POST['cadre_max_capacity']
        cadre_type_id = request.POST['cadre_type_id']
        type.cadre_type_id = get_object_or_404(CadreType, pk=cadre_type_id)
        type.save()
        return redirect('hausse_type_list')
    return render(request, 'hausse_types/update.html', {'type': type, 'cadre_types': cadre_types})


def hausse_type_delete(request, id):
    type = get_object_or_404(HausseType, pk=id)
    type.delete()
    return redirect('hausse_type_list')


# ----------------CRUD HAUSSE CADRE---------------------


def hausse_cadre_list(request):
    cadres = HausseCadre.objects.select_related(
        'hausse_id').order_by('-created_at')
    return render(request, 'hausse_cadres/list.html', {'cadres': cadres})


def hausse_cadre_detail(request, id):
    type = get_object_or_404(HausseCadre, pk=id)
    return render(request, 'hausse_cadres/detail.html', {'type': type})


def hausse_cadre_create(request):
    hausses = Hausse.objects.all()
    if request.method == 'POST':
        hausse_id = request.POST['hausse_id']
        added_cadre = request.POST['added_cadre']
        hausse = get_object_or_404(Hausse, pk=hausse_id)
        HausseCadre.objects.create(
            hausse_id=hausse, added_cadre=added_cadre, created_at=timezone.now())
        return redirect('hausse_cadre_list')
    return render(request, 'hausse_cadres/create.html', {'hausses': hausses})


def hausse_cadre_update(request, id):
    cadre = get_object_or_404(HausseCadre, pk=id)
    hausses = Hausse.objects.all()
    if request.method == 'POST':
        hausse_id = request.POST['hausse_id']
        cadre.added_cadre = request.POST['added_cadre']
        cadre.hausse_id = get_object_or_404(Hausse, pk=hausse_id)
        cadre.save()
        return redirect('hausse_cadre_list')
    return render(request, 'hausse_cadres/update.html', {'cadre': cadre, 'hausses': hausses})


def hausse_cadre_delete(request, id):
    cadre = get_object_or_404(HausseCadre, pk=id)
    cadre.delete()
    return redirect('hausse_cadre_list')


# -----------------CRUD HAUSSE---------------

def hausse_list(request):
    hausses = Hausse.objects.select_related('hausse_type_id')
    return render(request, 'hausses/list.html', {'hausses': hausses})


def hausse_detail(request, id):
    hausse = get_object_or_404(Hausse, pk=id)
    return render(request, 'hausses/detail.html', {'hausse': hausse})


def hausse_create(request):
    hausse_types = HausseType.objects.all()
    if request.method == 'POST':
        hausse_type_id = request.POST['hausse_type_id']
        hausse_type = get_object_or_404(HausseType, pk=hausse_type_id)
        Hausse.objects.create(hausse_type_id=hausse_type,
                              created_at=timezone.now())
        return redirect('hausse_list')
    return render(request, 'hausses/create.html', {'hausse_types': hausse_types})


def hausse_update(request, id):
    hausse = get_object_or_404(Hausse, pk=id)
    hausse_types = HausseType.objects.all()
    if request.method == 'POST':
        hausse_type_id = request.POST['hausse_type_id']
        hausse.hausse_type_id = get_object_or_404(
            HausseType, pk=hausse_type_id)
        hausse.save()
        return redirect('hausse_list')
    return render(request, 'hausses/update.html', {'hausse': hausse, 'hausse_types': hausse_types})


def hausse_delete(request, id):
    hausse = get_object_or_404(Hausse, pk=id)
    hausse.delete()
    return redirect('hausse_list')


# -------------CRUD RUCHE STATUS ---------------------

def ruche_status_list(request):
    statuses = RucheStatus.objects.all()
    return render(request, 'ruche_status/list.html', {'statuses': statuses})


def ruche_status_detail(request, id):
    status = get_object_or_404(RucheStatus, pk=id)
    return render(request, 'ruche_status/detail.html', {'status': status})


def ruche_status_create(request):
    if request.method == 'POST':
        name = request.POST['name']
        RucheStatus.objects.create(name=name)
        return redirect('ruche_status_list')
    return render(request, 'ruche_status/create.html')


def ruche_status_update(request, id):
    status = get_object_or_404(RucheStatus, pk=id)
    if request.method == 'POST':
        status.name = request.POST['name']
        status.save()
        return redirect('ruche_status_list')
    return render(request, 'ruche_status/update.html', {'status': status})


def ruche_status_delete(request, id):
    status = get_object_or_404(RucheStatus, pk=id)
    status.delete()
    return redirect('ruche_status_list')


# -------------CRUD RUCHE----------------

def ruche_list(request):
    ruches = Ruche.objects.select_related(
        'localizations_id', 'ruche_type_id', 'essaim_id')
    return render(request, 'ruches/list.html', {'ruches': ruches})


def ruche_detail(request, id):
    ruche = get_object_or_404(Ruche, pk=id)
    return render(request, 'ruches/detail.html', {'ruche': ruche})


def ruche_create(request):
    localizations = Localization.objects.all()
    ruche_types = RucheType.objects.all()
    essaims = Essaim.objects.all()
    if request.method == 'POST':
        description = request.POST['description']
        localization_id = request.POST['localization_id']
        ruche_type_id = request.POST['ruche_type_id']
        essaim_id = request.POST['essaim_id']
        localization = get_object_or_404(Localization, pk=localization_id)
        ruche_type = get_object_or_404(RucheType, pk=ruche_type_id)
        essaim = get_object_or_404(Essaim, pk=essaim_id)
        Ruche.objects.create(
            description=description,
            localizations_id=localization,
            ruche_type_id=ruche_type,
            essaim_id=essaim,
            created_at=timezone.now()
        )
        return redirect('ruche_list')
    return render(request, 'ruches/create.html', {'localizations': localizations, 'ruche_types': ruche_types, 'essaims': essaims})


def ruche_update(request, id):
    ruche = get_object_or_404(Ruche, pk=id)
    localizations = Localization.objects.all()
    ruche_types = RucheType.objects.all()
    essaims = Essaim.objects.all()
    if request.method == 'POST':
        ruche.description = request.POST['description']
        localization_id = request.POST['localization_id']
        ruche_type_id = request.POST['ruche_type_id']
        essaim_id = request.POST['essaim_id']
        ruche.localizations_id = get_object_or_404(
            Localization, pk=localization_id)
        ruche.ruche_type_id = get_object_or_404(RucheType, pk=ruche_type_id)
        ruche.essaim_id = get_object_or_404(Essaim, pk=essaim_id)
        ruche.save()
        return redirect('ruche_list')
    return render(request, 'ruches/update.html', {'ruche': ruche, 'localizations': localizations, 'ruche_types': ruche_types, 'essaims': essaims})


def ruche_delete(request, id):
    ruche = get_object_or_404(Ruche, pk=id)
    ruche.delete()
    return redirect('ruche_list')

# --------------CRUD ESSAIM ORIGIN -------------------


def essaim_origin_list(request):
    origins = EssaimOrigin.objects.all()
    return render(request, 'essaim_origins/list.html', {'origins': origins})


def essaim_origin_detail(request, id):
    origin = get_object_or_404(EssaimOrigin, pk=id)
    return render(request, 'essaim_origins/detail.html', {'origin': origin})


def essaim_origin_create(request):
    if request.method == 'POST':
        name = request.POST['name']
        EssaimOrigin.objects.create(name=name)
        return redirect('essaim_origin_list')
    return render(request, 'essaim_origins/create.html')


def essaim_origin_update(request, id):
    origin = get_object_or_404(EssaimOrigin, pk=id)
    if request.method == 'POST':
        origin.name = request.POST['name']
        origin.save()
        return redirect('essaim_origin_list')
    return render(request, 'essaim_origins/update.html', {'origin': origin})


def essaim_origin_delete(request, id):
    origin = get_object_or_404(EssaimOrigin, pk=id)
    origin.delete()
    return redirect('essaim_origin_list')

# --------------CRUD ESSAIM RACE-------------


def essaim_race_list(request):
    races = EssaimRace.objects.all()
    return render(request, 'essaim_races/list.html', {'races': races})


def essaim_race_detail(request, id):
    race = get_object_or_404(EssaimRace, pk=id)
    return render(request, 'essaim_races/detail.html', {'race': race})


def essaim_race_create(request):
    if request.method == 'POST':
        name = request.POST['name']
        EssaimRace.objects.create(name=name)
        return redirect('essaim_race_list')
    return render(request, 'essaim_races/create.html')


def essaim_race_update(request, id):
    race = get_object_or_404(EssaimRace, pk=id)
    if request.method == 'POST':
        race.name = request.POST['name']
        race.save()
        return redirect('essaim_race_list')
    return render(request, 'essaim_races/update.html', {'race': race})


def essaim_race_delete(request, id):
    race = get_object_or_404(EssaimRace, pk=id)
    race.delete()
    return redirect('essaim_race_list')

# ----------------CRUD ESSAIM STATUS------------------


def essaim_status_list(request):
    statuses = EssaimStatus.objects.all()
    return render(request, 'essaim_status/list.html', {'statuses': statuses})


def essaim_status_detail(request, id):
    status = get_object_or_404(EssaimStatus, pk=id)
    return render(request, 'essaim_status/detail.html', {'status': status})


def essaim_status_create(request):
    if request.method == 'POST':
        name = request.POST['name']
        EssaimStatus.objects.create(name=name)
        return redirect('essaim_status_list')
    return render(request, 'essaim_status/create.html')


def essaim_status_update(request, id):
    status = get_object_or_404(EssaimStatus, pk=id)
    if request.method == 'POST':
        status.name = request.POST['name']
        status.save()
        return redirect('essaim_status_list')
    return render(request, 'essaim_status/update.html', {'status': status})


def essaim_status_delete(request, id):
    status = get_object_or_404(EssaimStatus, pk=id)
    status.delete()
    return redirect('essaim_status_list')


# ------------------CRUD ESSAIM DETAIL------------------


def essaim_detail_list(request):
    details = EssaimDetail.objects.select_related('essaim_id')
    return render(request, 'essaim_details/list.html', {'details': details})


def essaim_detail_detail(request, id):
    detail = get_object_or_404(EssaimDetail, pk=id)
    return render(request, 'essaim_details/detail.html', {'detail': detail})


def essaim_detail_create(request):
    essaims = Essaim.objects.all()
    if request.method == 'POST':
        essaim_id = request.POST['essaim_id']
        note = request.POST['note']
        is_death = 'is_death' in request.POST
        ouvrier_added = request.POST['ouvrier_added']
        faux_bourdon_added = request.POST['faux_bourdon_added']
        reine_added = request.POST['reine_added']
        essaim = get_object_or_404(Essaim, pk=essaim_id)
        EssaimDetail.objects.create(
            essaim_id=essaim,
            note=note,
            is_death=is_death,
            ouvrier_added=ouvrier_added,
            faux_bourdon_added=faux_bourdon_added,
            reine_added=reine_added,
            created_at=timezone.now()
        )
        return redirect('essaim_detail_list')
    return render(request, 'essaim_details/create.html', {'essaims': essaims})


def essaim_detail_update(request, id):
    detail = get_object_or_404(EssaimDetail, pk=id)
    essaims = Essaim.objects.all()
    if request.method == 'POST':
        essaim_id = request.POST['essaim_id']
        detail.note = request.POST['note']
        detail.is_death = 'is_death' in request.POST
        detail.ouvrier_added = request.POST['ouvrier_added']
        detail.faux_bourdon_added = request.POST['faux_bourdon_added']
        detail.reine_added = request.POST['reine_added']
        detail.essaim_id = get_object_or_404(Essaim, pk=essaim_id)
        detail.save()
        return redirect('essaim_detail_list')
    return render(request, 'essaim_details/update.html', {'detail': detail, 'essaims': essaims})


def essaim_detail_delete(request, id):
    detail = get_object_or_404(EssaimDetail, pk=id)
    detail.delete()
    return redirect('essaim_detail_list')


# ---------------CRUD ESSAIM SANTE HISTORIES------------------

def essaim_sante_history_list(request):
    histories = EssaimSanteHistory.objects.select_related(
        'essaim_id', 'comportement_id').order_by('-created_at')
    return render(request, 'essaim_sante_histories/list.html', {'histories': histories})


def essaim_sante_history_detail(request, id):
    history = get_object_or_404(EssaimSanteHistory, pk=id)
    return render(request, 'essaim_sante_histories/detail.html', {'history': history})


def essaim_sante_history_create(request):
    essaims = Essaim.objects.all()
    comportements = Comportement.objects.all()
    if request.method == 'POST':
        essaim_id = request.POST['essaim_id']
        comportement_id = request.POST['comportement_id']
        force_colonie = request.POST['force_colonie']
        egg_present = 'egg_present' in request.POST
        couvain_present = 'couvain_present' in request.POST
        reine_present = 'reine_present' in request.POST
        parasite = request.POST['parasite']
        maladie = request.POST['maladie']
        note = request.POST['note']
        essaim = get_object_or_404(Essaim, pk=essaim_id)
        comportement = get_object_or_404(Comportement, pk=comportement_id)
        EssaimSanteHistory.objects.create(
            essaim_id=essaim,
            comportement_id=comportement,
            force_colonie=force_colonie,
            egg_present=egg_present,
            couvain_present=couvain_present,
            reine_present=reine_present,
            parasite=parasite,
            maladie=maladie,
            note=note,
            created_at=timezone.now()
        )
        return redirect('essaim_sante_history_list')
    return render(request, 'essaim_sante_histories/create.html', {'essaims': essaims, 'comportements': comportements})


def essaim_sante_history_update(request, id):
    history = get_object_or_404(EssaimSanteHistory, pk=id)
    essaims = Essaim.objects.all()
    comportements = Comportement.objects.all()
    if request.method == 'POST':
        essaim_id = request.POST['essaim_id']
        comportement_id = request.POST['comportement_id']
        history.force_colonie = request.POST['force_colonie']
        history.egg_present = 'egg_present' in request.POST
        history.couvain_present = 'couvain_present' in request.POST
        history.reine_present = 'reine_present' in request.POST
        history.parasite = request.POST['parasite']
        history.maladie = request.POST['maladie']
        history.note = request.POST['note']
        history.essaim_id = get_object_or_404(Essaim, pk=essaim_id)
        history.comportement_id = get_object_or_404(
            Comportement, pk=comportement_id)
        history.save()
        return redirect('essaim_sante_history_list')
    return render(request, 'essaim_sante_histories/update.html', {'history': history, 'essaims': essaims, 'comportements': comportements})


def essaim_sante_history_delete(request, id):
    history = get_object_or_404(EssaimSanteHistory, pk=id)
    history.delete()
    return redirect('essaim_sante_history_list')


# ---------------CRUD COMPORTEMENT-----------------

def comportement_list(request):
    comportements = Comportement.objects.all()
    return render(request, 'comportements/list.html', {'comportements': comportements})


def comportement_detail(request, id):
    comportement = get_object_or_404(Comportement, pk=id)
    return render(request, 'comportements/detail.html', {'comportement': comportement})


def comportement_create(request):
    if request.method == 'POST':
        description = request.POST['description']
        Comportement.objects.create(description=description)
        return redirect('comportement_list')
    return render(request, 'comportements/create.html')


def comportement_update(request, id):
    comportement = get_object_or_404(Comportement, pk=id)
    if request.method == 'POST':
        comportement.description = request.POST['description']
        comportement.save()
        return redirect('comportement_list')
    return render(request, 'comportements/update.html', {'comportement': comportement})


def comportement_delete(request, id):
    comportement = get_object_or_404(Comportement, pk=id)
    comportement.delete()
    return redirect('comportement_list')

# --------------CRUD ESSAIM-----------------


def essaim_list(request):
    essaims = Essaim.objects.select_related(
        'essaim_origin_id', 'essaim_race_id')
    return render(request, 'essaims/list.html', {'essaims': essaims})


def essaim_detail(request, id):
    essaim = get_object_or_404(Essaim, pk=id)
    return render(request, 'essaims/detail.html', {'essaim': essaim})


def essaim_create(request):
    origins = EssaimOrigin.objects.all()
    races = EssaimRace.objects.all()
    if request.method == 'POST':
        origin_id = request.POST['origin_id']
        race_id = request.POST['race_id']
        origin = get_object_or_404(EssaimOrigin, pk=origin_id)
        race = get_object_or_404(EssaimRace, pk=race_id)
        Essaim.objects.create(essaim_origin_id=origin,
                              essaim_race_id=race, created_at=timezone.now())
        return redirect('essaim_list')
    return render(request, 'essaims/create.html', {'origins': origins, 'races': races})


def essaim_update(request, id):
    essaim = get_object_or_404(Essaim, pk=id)
    origins = EssaimOrigin.objects.all()
    races = EssaimRace.objects.all()
    if request.method == 'POST':
        origin_id = request.POST['origin_id']
        race_id = request.POST['race_id']
        essaim.essaim_origin_id = get_object_or_404(EssaimOrigin, pk=origin_id)
        essaim.essaim_race_id = get_object_or_404(EssaimRace, pk=race_id)
        essaim.save()
        return redirect('essaim_list')
    return render(request, 'essaims/update.html', {'essaim': essaim, 'origins': origins, 'races': races})


def essaim_delete(request, id):
    essaim = get_object_or_404(Essaim, pk=id)
    essaim.delete()
    return redirect('essaim_list')

# ---------------CRUD LOCALIZATION STATUS HISTORY----------------


def localization_status_history_list(request):
    histories = LocalizationStatusHistory.objects.select_related(
        'localization_id', 'localization_status_id').order_by('-created_at')
    return render(request, 'localization_status_histories/list.html', {'histories': histories})


def localization_status_history_detail(request, id):
    history = get_object_or_404(LocalizationStatusHistory, pk=id)
    return render(request, 'localization_status_histories/detail.html', {'history': history})


def localization_status_history_create(request):
    localizations = Localization.objects.all()
    statuses = LocalizationStatus.objects.all()
    if request.method == 'POST':
        localization_id = request.POST['localization_id']
        status_id = request.POST['localization_status_id']
        localization = get_object_or_404(Localization, pk=localization_id)
        status = get_object_or_404(LocalizationStatus, pk=status_id)
        LocalizationStatusHistory.objects.create(
            localization_id=localization, localization_status_id=status, created_at=timezone.now())
        return redirect('localization_status_history_list')
    return render(request, 'localization_status_histories/create.html', {'localizations': localizations, 'statuses': statuses})


def localization_status_history_update(request, id):
    history = get_object_or_404(LocalizationStatusHistory, pk=id)
    localizations = Localization.objects.all()
    statuses = LocalizationStatus.objects.all()
    if request.method == 'POST':
        localization_id = request.POST['localization_id']
        status_id = request.POST['localization_status_id']
        history.localization_id = get_object_or_404(
            Localization, pk=localization_id)
        history.localization_status_id = get_object_or_404(
            LocalizationStatus, pk=status_id)
        history.save()
        return redirect('localization_status_history_list')
    return render(request, 'localization_status_histories/update.html', {
        'history': history,
        'localizations': localizations,
        'statuses': statuses
    })


def localization_status_history_delete(request, id):
    history = get_object_or_404(LocalizationStatusHistory, pk=id)
    history.delete()
    return redirect('localization_status_history_list')

# -----------------CRUD RUCHE HAUSSE HISTORY---------------


def ruche_hausse_history_list(request):
    histories = RucheHausseHistory.objects.select_related(
        'ruche_id', 'hausse_id').order_by('-created_at')
    return render(request, 'ruche_hausse_histories/list.html', {'histories': histories})


def ruche_hausse_history_detail(request, id):
    history = get_object_or_404(RucheHausseHistory, pk=id)
    return render(request, 'ruche_hausse_histories/detail.html', {'history': history})


def ruche_hausse_history_create(request):
    ruches = Ruche.objects.all()
    hausses = Hausse.objects.all()
    if request.method == 'POST':
        ruche_id = request.POST['ruche_id']
        hausse_id = request.POST['hausse_id']
        is_removed = 'is_removed' in request.POST
        ruche = get_object_or_404(Ruche, pk=ruche_id)
        hausse = get_object_or_404(Hausse, pk=hausse_id)
        RucheHausseHistory.objects.create(
            ruche_id=ruche, hausse_id=hausse, is_removed=is_removed, created_at=timezone.now())
        return redirect('ruche_hausse_history_list')
    return render(request, 'ruche_hausse_histories/create.html', {'ruches': ruches, 'hausses': hausses})


def ruche_hausse_history_update(request, id):
    history = get_object_or_404(RucheHausseHistory, pk=id)
    ruches = Ruche.objects.all()
    hausses = Hausse.objects.all()
    if request.method == 'POST':
        ruche_id = request.POST['ruche_id']
        hausse_id = request.POST['hausse_id']
        history.is_removed = 'is_removed' in request.POST
        history.ruche_id = get_object_or_404(Ruche, pk=ruche_id)
        history.hausse_id = get_object_or_404(Hausse, pk=hausse_id)
        history.save()
        return redirect('ruche_hausse_history_list')
    return render(request, 'ruche_hausse_histories/update.html', {'history': history, 'ruches': ruches, 'hausses': hausses})


def ruche_hausse_history_delete(request, id):
    history = get_object_or_404(RucheHausseHistory, pk=id)
    history.delete()
    return redirect('ruche_hausse_history_list')


# -------------------- CRUD RUCHE STATUS HISTORY --------------------

def ruche_status_history_list(request):
    histories = RucheStatusHistory.objects.select_related(
        'ruche_id', 'ruche_status_id').order_by('-created_at')
    return render(request, 'ruche_status_histories/list.html', {'histories': histories})


def ruche_status_history_detail(request, id):
    history = get_object_or_404(RucheStatusHistory, pk=id)
    return render(request, 'ruche_status_histories/detail.html', {'history': history})


def ruche_status_history_create(request):
    ruches = Ruche.objects.all()
    statuses = RucheStatus.objects.all()
    if request.method == 'POST':
        ruche_id = request.POST['ruche_id']
        status_id = request.POST['ruche_status_id']
        ruche = get_object_or_404(Ruche, pk=ruche_id)
        status = get_object_or_404(RucheStatus, pk=status_id)
        RucheStatusHistory.objects.create(
            ruche_id=ruche, ruche_status_id=status, created_at=timezone.now())
        return redirect('ruche_status_history_list')
    return render(request, 'ruche_status_histories/create.html', {'ruches': ruches, 'statuses': statuses})


def ruche_status_history_update(request, id):
    history = get_object_or_404(RucheStatusHistory, pk=id)
    ruches = Ruche.objects.all()
    statuses = RucheStatus.objects.all()
    if request.method == 'POST':
        ruche_id = request.POST['ruche_id']
        status_id = request.POST['ruche_status_id']
        history.ruche_id = get_object_or_404(Ruche, pk=ruche_id)
        history.ruche_status_id = get_object_or_404(RucheStatus, pk=status_id)
        history.save()
        return redirect('ruche_status_history_list')
    return render(request, 'ruche_status_histories/update.html', {
        'history': history,
        'ruches': ruches,
        'statuses': statuses
    })


def ruche_status_history_delete(request, id):
    history = get_object_or_404(RucheStatusHistory, pk=id)
    history.delete()
    return redirect('ruche_status_history_list')
