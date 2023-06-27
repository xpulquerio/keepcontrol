from django.shortcuts import render, get_object_or_404
from .models import Serie, SeasonSerie, EpisodeSerie
from django.contrib.auth import get_user_model #Para usar o model do nosso usuário
from django.contrib.auth.decorators import login_required

User = get_user_model()

# Create your models here.

def series (request):
    context = {}
    series = Serie.objects.all()
    qtd_series = len(series)

    for serie in series:
        temp_count = SeasonSerie.get_qtd_seasons(serie.id)
        serie.qtd_temps = temp_count
    
    template_name = 'series.html'
    context['series'] = series
    context['qtd_series'] = qtd_series

    return render(request, template_name, context)

def serie_details (request, id):
    context = {}

    serie = get_object_or_404(Serie, id=id)
    serie.qtd_temps = SeasonSerie.get_qtd_seasons(id) #Incluindo quantidade de temporadas como atributo de serie
    serie.qtd_total_eps = 0

    seasons = SeasonSerie.objects.filter(serie_id=id).order_by('pt_title')
    for season in seasons:
        season.qtd_eps = EpisodeSerie.get_qtd_episodes(season.id)
        serie.qtd_total_eps += season.qtd_eps

    context['seasons'] = seasons
    context['serie'] = serie
    template_name = 'serie_details.html'

    return render(request, template_name, context)

@login_required
def season_details (request, serie_id, season_id):
    context = {}
    
    season = SeasonSerie.objects.filter(id=season_id)
    serie = Serie.objects.filter(id=serie_id)
    eps = EpisodeSerie.objects.filter(season_id=season_id).order_by('number')
    
    usuario = request.user #Pegando o usuário logado
    
    for ep in eps:
        user_episode = ep.userepisodeserie_set.filter(user=usuario.id).first()
        if user_episode and user_episode.date_watched:
            ep.date_watched = user_episode.date_watched
    
    context['eps'] = eps
    context['season'] = season[0].pt_title
    context['serie'] = serie[0].pt_title
    template_name = 'season_details.html'
    
    return render(request, template_name, context)