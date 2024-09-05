from django.shortcuts import render, get_object_or_404, redirect
from .models import Serie, SeasonSerie, EpisodeSerie
from apps.accounts.models import UserEpisodeSerie, FavoriteSerie
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q

def ListSerie (request):
    
    search_query = request.GET.get('search') #Link com o form-serch no html
    
    if search_query:
        series = Serie.objects.filter(
            Q(pt_title__icontains=search_query) |  # Busca por título em português (case-insensitive)
            Q(or_title__icontains=search_query)    # Busca por título em inglês (case-insensitive)
        ).order_by('or_title')
    else:
        series = Serie.objects.all().order_by('-created_at')    
    
    #FAVORITOS
    user_id = request.user.id
    if user_id:
        favoritos = FavoriteSerie.objects.filter(user_id=user_id)
    else:
        favoritos = []
    

    for serie in series:
        temp_count = SeasonSerie.get_qtd_seasons(serie.id)
        serie.qtd_temps = temp_count

        for temp in favoritos: #Verifica quais animes já estão favoritados
            if temp.serie_id == serie.id and temp.user_id == user_id:
                serie.favorite = True
        
    
    movies_paginator = Paginator(series, 20) #Filtra apenas 20 de todos os animes
    
    page_num = request.GET.get('page')
   
    page = movies_paginator.get_page(page_num)
    
    
    template_name = 'ListSerie.html'
    context = {
        'page' : page,
        'qtd_series' : series.count
    }
    
    return render(request, template_name, context)

def ListSeasonSerie (request, id):
    context = {}

    serie = get_object_or_404(Serie, id=id)
    serie.qtd_temps = SeasonSerie.get_qtd_seasons(id) #Incluindo quantidade de temporadas como atributo de serie
    serie.qtd_total_eps = 0

    seasons = SeasonSerie.objects.filter(serie_id=id).order_by('number')
    for season in seasons:
        season.qtd_assistido = 0
        season.qtd_eps = EpisodeSerie.get_qtd_episodes(season.id)
        serie.qtd_total_eps += season.qtd_eps
        if request.user.is_authenticated:
            epsisodes = EpisodeSerie.objects.filter(season=season.id)
            for ep in epsisodes:
                if ep in request.user.episodes_serie.all():
                    season.qtd_assistido += 1

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
    
    template_name = 'ListEpisodeSerie.html'
    
    # pegado last season of the serie
    number_season = SeasonSerie.objects.filter(id=season_id).first().number #Numero da season que clicou
    quantidade_de_seasons = SeasonSerie.objects.filter(serie_id=serie_id).count() #Quantidade de Seasons
    
    last_season = False

    if number_season == quantidade_de_seasons: #Se a última season adicionar for igual a quantidade de seasons TRUE
        last_season = True
 

    context = {
        'eps': eps,
        'season': season.first(),
        'serie': serie.first(),
        'last_season': last_season
    }

    return render(request, template_name, context)

@login_required
def InserirAssistidoEpisodeSerie(request, episodeserie_id):
    episodio_serie = EpisodeSerie.objects.filter(id=episodeserie_id).first()
    season_id = episodio_serie.season.id
    serie_id = episodio_serie.season.serie_id
    
    usuario = request.user
    episodeserie_user = UserEpisodeSerie.objects.filter(user=usuario.id, episode=episodeserie_id)
    if episodeserie_user:
        print (str(episodeserie_user)+" já foi assistido pelo usuário")
        return redirect('series:ListEpisodeSerie', serie_id=serie_id, season_id=season_id )
    else:
        episodeserie_user = UserEpisodeSerie(episode=episodio_serie, user=usuario, date_watched=timezone.now()) #Depois alterar o banco para inserir a data automaticamente
        episodeserie_user.save()
        print (str(episodio_serie)+" inserido!")
        return redirect('series:ListEpisodeSerie', serie_id=serie_id, season_id=season_id )
    
@login_required
def InserirAssistidoSeasonSerie(request, season_id, serie_id):
    episodes_serie = EpisodeSerie.objects.filter(season=season_id)
    
    for ep in episodes_serie:
        ep_id = ep.id
        print(ep_id)
        InserirAssistidoEpisodeSerie(request=request,episodeserie_id=ep_id)
        
    return redirect('series:ListSeasonSerie', id=serie_id)

@login_required
def InserirSerieFavorita(request, serie_id):
    #Insere a serie como favorito!
    
    usuario = request.user
    seriefavorita_user = FavoriteSerie.objects.filter(user=usuario.id, serie_id=serie_id)
        
    if seriefavorita_user:
        print (str(seriefavorita_user)+" já foi favoritada pelo usuário")
        return redirect('series:ListSerie')
    else:
        x = FavoriteSerie(user=usuario, serie_id=serie_id)
        x.save()
        print (str(x)+" favoritada!")
        return redirect('series:ListSerie')
    
@login_required
def AdicionarNovoEP(request, season_id, serie_id):
    #Pegar número do último episódio da temporada
    try:
        x = EpisodeSerie.objects.filter(season_id=season_id).order_by('number').last().number
    except:
        x = 0
    #Soma +1 ao número do episódio
    x = x+1

    #Cria um novo episódio para aquela temporada
    novo_ep = EpisodeSerie(number=x, season_id=season_id)
    #Salvar esse novo episódio
    novo_ep.save()
        
    return redirect('series:ListEpisodeSerie', serie_id=serie_id, season_id=season_id)