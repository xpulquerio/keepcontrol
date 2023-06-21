from django.shortcuts import render, get_object_or_404
from .models import Serie
from apps.core.models import Season
from apps.core.models import Episode
# Create your models here.

def series (request):
    context = {}
    series = Serie.objects.all()
    qtd_series = len(series)

    for serie in series:
        temp_count = Season.get_qtd_seasons(serie.id)
        serie.qtd_temps = temp_count
    
    template_name = 'series.html'
    context['series'] = series
    context['qtd_series'] = qtd_series

    return render(request, template_name, context)

def details (request, id):
    context = {}

    serie = get_object_or_404(Serie, id=id)
    serie.qtd_temps = Season.get_qtd_seasons(id) #Incluindo quantidade de temporadas como atributo de serie
    serie.qtd_total_eps = 0

    seasons = Season.get_seasons(id_da_serie=id)
    for season in seasons:
        season.qtd_eps = Episode.get_qtd_episodes(season.id)
        serie.qtd_total_eps += season.qtd_eps

    context['seasons'] = seasons
    context['serie'] = serie
    template_name = 'details.html'

    

    return render(request, template_name, context)