from django.shortcuts import render, get_object_or_404, redirect
from .models import Anime, SeasonAnime, EpisodeAnime
from apps.accounts.models import UserEpisodeAnime, FavoriteAnime
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q

def ListAnime (request):
    
    search_query = request.GET.get('search') #Link com o form-serch no html
    
    if search_query:
        animes = Anime.objects.filter(
            Q(pt_title__icontains=search_query) |  # Busca por título em português (case-insensitive)
            Q(or_title__icontains=search_query)    # Busca por título em inglês (case-insensitive)
        ).order_by('or_title')
    else:
        animes = Anime.objects.all().order_by('-created_at')    
    
    user_id = request.user.id
    if user_id:
        favoritos = FavoriteAnime.objects.filter(user_id=user_id)
    else:
        favoritos = []
    
    for anime in animes:
        temp_count = SeasonAnime.get_qtd_seasons(anime.id)
        anime.qtd_temps = temp_count
        
        anime.descricao_completa()
                
        for temp in favoritos: #Verifica quais animes já estão favoritados
            if temp.anime_id == anime.id and temp.user_id == user_id:
                anime.favorite = True
        
    movies_paginator = Paginator(animes, 20) #Filtra apenas 20 de todos os animes
    
    page_num = request.GET.get('page')
   
    page = movies_paginator.get_page(page_num)
    
    template_name = 'ListAnime.html'
    context = {
        'page': page,
        'qtd_animes' : animes.count,
        'qtd_pages': movies_paginator.num_pages,
        'search_query': search_query  # Passar o valor de busca para o template
    }

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
    
    template_name = 'ListSeasonAnime.html'
    
    context = {
        'seasons': seasons,
        'anime': anime,
        
    }    

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
    
    # pegado last season of the anime
    number_season = SeasonAnime.objects.filter(id=season_id).first().number #Numero da season que clicou
    quantidade_de_seasons = SeasonAnime.objects.filter(anime_id=anime_id).count() #Quantidade de Seasons
    
    last_season = False

    if number_season == quantidade_de_seasons: #Se a última season adicionar for igual a quantidade de seasons TRUE
        last_season = True

    context['last_season'] = last_season
    context['eps'] = eps
    context['season'] = season.first()
    context['anime'] = anime.first()
    template_name = 'ListEpisodeAnime.html'
    
    return render(request, template_name, context)

@login_required
def InserirAssistidoEpisodeAnime(request, episode_id):
    #Insere um episódio do anime como assistido pelo usuário logado!
    episodio_anime = EpisodeAnime.objects.filter(id=episode_id).first()
    season_id = episodio_anime.season.id
    anime_id = episodio_anime.season.anime_id
    
    if (False):
        date = '2021-01-14 00:00:00'
    else:
        date = timezone.now()

    usuario = request.user
    episodeanime_user = UserEpisodeAnime.objects.filter(user=usuario.id, episode=episode_id)
        
    if episodeanime_user:
        #print (str(episodeanime_user)+" já foi assistido pelo usuário")
        return redirect('animes:ListEpisodeAnime', anime_id=anime_id, season_id=season_id)
    else:
        x = UserEpisodeAnime(episode=episodio_anime, user=usuario, date_watched=date) #timezone.now()Depois alterar o banco para inserir a data automaticamente
        x.save()
        #print (str(episodio_anime)+" inserido!")
        return redirect('animes:ListEpisodeAnime', anime_id=anime_id, season_id=season_id)

@login_required
def InserirAssistidoSeasonAnime(request, season_id, anime_id):
    #Insere todos os episódios de uma temporada de um anime como assistidos pelo usuário logado!
    episodes_anime = EpisodeAnime.objects.filter(season=season_id)
    
    for ep in episodes_anime:
        x = ep.id
        print(x)
        InserirAssistidoEpisodeAnime(request=request,episode_id=x)
        
    return redirect('animes:ListSeasonAnime', id=anime_id)

@login_required
def InserirAnimeFavorito(request, anime_id):
    #Insere o anime como favorito!
    
    usuario = request.user
    animefavorito_user = FavoriteAnime.objects.filter(user=usuario.id, anime_id=anime_id)
        
    if animefavorito_user:
        print (str(animefavorito_user)+" já foi favoritado pelo usuário")
        return redirect('animes:ListAnime')
    else:
        x = FavoriteAnime(user=usuario, anime_id=anime_id)
        x.save()
        print (str(x)+" favoritado!")
        return redirect('animes:ListAnime')

@login_required
def AdicionarNovoEP(request, season_id, anime_id):
    
    #Pegar número do último episódio da temporada e não tiver último zera

    try:
        x = EpisodeAnime.objects.filter(season_id=season_id).order_by('number').last().number
    except:
        x = 0
    
    #Soma +1 ao número do episódio
    x = x+1
    #Cria um novo episódio para aquela temporada
    novo_ep = EpisodeAnime(number=x, season_id=season_id)
    #Salvar esse novo episódio
    novo_ep.save()
        
    return redirect('animes:ListEpisodeAnime', anime_id=anime_id, season_id=season_id)