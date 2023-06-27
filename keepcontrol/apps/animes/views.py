from django.shortcuts import render, get_object_or_404
from .models import Anime, SeasonAnime, EpisodeAnime

from django.contrib.auth import get_user_model #Para usar o model do nosso usuário
from django.contrib.auth.decorators import login_required

User = get_user_model()

# Create your models here.

def animes (request):
    context = {}
    animes = Anime.objects.all()
    qtd_animes = len(animes)

    for anime in animes:
        temp_count = SeasonAnime.get_qtd_seasons(anime.id)
        anime.qtd_temps = temp_count
    
    template_name = 'animes.html'
    context['animes'] = animes
    context['qtd_animes'] = qtd_animes

    return render(request, template_name, context)

def anime_details (request, id):
    context = {}

    anime = get_object_or_404(Anime, id=id)
    anime.qtd_temps = SeasonAnime.get_qtd_seasons(id) #Incluindo quantidade de temporadas como atributo de anime
    anime.qtd_total_eps = 0

    seasons = SeasonAnime.objects.filter(anime_id=id).order_by('pt_title')
    for season in seasons:
        season.qtd_eps = EpisodeAnime.get_qtd_episodes(season.id)
        anime.qtd_total_eps += season.qtd_eps

    context['seasons'] = seasons
    context['anime'] = anime
    template_name = 'anime_details.html'

    return render(request, template_name, context)

@login_required
def season_details (request, anime_id, season_id):
    context = {}
    
    season = SeasonAnime.objects.filter(id=season_id)
    anime = Anime.objects.filter(id=anime_id)
    eps = EpisodeAnime.objects.filter(season_id=season_id).order_by('number')
    
    usuario = request.user #Pegando o usuário logado
    
    for ep in eps:
        user_episode = ep.userepisodeanime_set.filter(user=usuario.id).first()
        if user_episode and user_episode.date_watched:
            ep.date_watched = user_episode.date_watched
    
    context['eps'] = eps
    context['season'] = season[0].pt_title
    context['anime'] = anime[0].pt_title
    template_name = 'season_details.html'
    
    return render(request, template_name, context)