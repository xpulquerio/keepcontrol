from django.shortcuts import render, get_object_or_404, redirect
from .models import Anime, SeasonAnime, EpisodeAnime
from apps.accounts.models import UserEpisodeAnime
from django.contrib.auth.decorators import login_required
from django.utils import timezone

def ListAnime (request):
    context = {}
    animes = Anime.objects.all()
    qtd_animes = len(animes)

    for anime in animes:
        temp_count = SeasonAnime.get_qtd_seasons(anime.id)
        anime.qtd_temps = temp_count
    
    template_name = 'ListAnime.html'
    context['animes'] = animes
    context['qtd_animes'] = qtd_animes

    return render(request, template_name, context)

def ListSeasonAnime (request, id):
    context = {}

    anime = get_object_or_404(Anime, id=id)
    anime.qtd_temps = SeasonAnime.get_qtd_seasons(id) #Incluindo quantidade de temporadas como atributo de anime
    anime.qtd_total_eps = 0

    seasons = SeasonAnime.objects.filter(anime_id=id).order_by('number')
        
    for season in seasons:
        season.qtd_assistido = 0
        season.qtd_eps = EpisodeAnime.get_qtd_episodes(season.id)
        anime.qtd_total_eps += season.qtd_eps
        if request.user.is_authenticated:
            epsisodes = EpisodeAnime.objects.filter(season=season.id)
            for ep in epsisodes:
                if ep in request.user.episodes_anime.all():
                    season.qtd_assistido += 1
        
    context['seasons'] = seasons
    context['anime'] = anime
    template_name = 'ListSeasonAnime.html'

    return render(request, template_name, context)

def ListEpisodeAnime (request, anime_id, season_id):
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
    context['season'] = season.first()
    context['anime'] = anime.first()
    template_name = 'ListEpisodeAnime.html'
    
    return render(request, template_name, context)

@login_required
def InserirAssistidoEpisodeAnime(request, episode_id):
    episodio_anime = EpisodeAnime.objects.filter(id=episode_id).first()
    season_id = episodio_anime.season.id
    anime_id = episodio_anime.season.anime_id
    
    usuario = request.user
    episodeanime_user = UserEpisodeAnime.objects.filter(user=usuario.id, episode=episode_id)
    
    if episodeanime_user:
        print (str(episodeanime_user)+" já foi assistido pelo usuário")
        return redirect('animes:ListEpisodeAnime', anime_id=anime_id, season_id=season_id)
    else:
        x = UserEpisodeAnime(episode=episodio_anime, user=usuario, date_watched=timezone.now()) #Depois alterar o banco para inserir a data automaticamente
        x.save()
        print (str(episodio_anime)+" inserido!")
        return redirect('animes:ListEpisodeAnime', anime_id=anime_id, season_id=season_id)

@login_required
def InserirAssistidoSeasonAnime(request, season_id, anime_id):
    episodes_anime = EpisodeAnime.objects.filter(season=season_id)
    
    for ep in episodes_anime:
        x = ep.id
        print(x)
        InserirAssistidoEpisodeAnime(request=request,episode_id=x)
        
    return redirect('animes:ListSeasonAnime', id=anime_id)
        