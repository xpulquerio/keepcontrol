from django.shortcuts import render, get_object_or_404, redirect
from .models import Serie, SeasonSerie, EpisodeSerie
from apps.accounts.models import UserEpisodeSerie
from django.contrib.auth.decorators import login_required
from django.utils import timezone

def ListSerie (request):
    context = {}
    series = Serie.objects.all()
    qtd_series = len(series)

    for serie in series:
        temp_count = SeasonSerie.get_qtd_seasons(serie.id)
        serie.qtd_temps = temp_count
    
    template_name = 'ListSerie.html'
    context['series'] = series
    context['qtd_series'] = qtd_series

    return render(request, template_name, context)

def ListSeasonSerie (request, id):
    context = {}

    serie = get_object_or_404(Serie, id=id)
    serie.qtd_temps = SeasonSerie.get_qtd_seasons(id) #Incluindo quantidade de temporadas como atributo de serie
    serie.qtd_total_eps = 0

    seasons = SeasonSerie.objects.filter(serie_id=id).order_by('number')
    for season in seasons:
        season.qtd_eps = EpisodeSerie.get_qtd_episodes(season.id)
        serie.qtd_total_eps += season.qtd_eps

    context['seasons'] = seasons
    context['serie'] = serie
    template_name = 'ListSeasonSerie.html'

    return render(request, template_name, context)

def ListEpisodeSerie (request, serie_id, season_id):
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
    context['season'] = season[0]
    context['serie'] = serie[0]
    template_name = 'ListEpisodeSerie.html'
    
    return render(request, template_name, context)

@login_required
def InserirAssistido(request, episodeserie_id):
    episodio_serie = EpisodeSerie.objects.filter(id=episodeserie_id).first()
    season_id = episodio_serie.season.id
    serie_id = episodio_serie.season.serie_id
    
    usuario = request.user
    episodeserie_user = UserEpisodeSerie.objects.filter(user=usuario.id, episode=episodeserie_id)
    if episodeserie_user:
        print (str(episodeserie_user)+" já foi assistido pelo usuário")
        return redirect('series:ListEpisodeSerie', serie_id=serie_id, season_id=season_id )
    else:
        x = UserEpisodeSerie(episode=episodio_serie, user=usuario, date_watched=timezone.now()) #Depois alterar o banco para inserir a data automaticamente
        #x.save()
        print (str(x)+" inserido!")
        return redirect('series:ListEpisodeSerie', serie_id=serie_id, season_id=season_id )