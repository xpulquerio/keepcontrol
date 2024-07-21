from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.conf import settings
from .forms import *
from apps.movies.models import Movie
from apps.series.models import EpisodeSerie, Serie, SeasonSerie
from apps.animes.models import EpisodeAnime, Anime, SeasonAnime
from apps.mangas.models import ChapterManga, Manga, VolumeManga
from apps.books.models import Book
from .models import UserEpisodeAnime, UserEpisodeSerie, UserMovie, UserChapterManga, UserBook, FavoriteManga, FavoriteAnime, FavoriteBook, FavoriteMovie, FavoriteSerie, FavoritesView
from itertools import chain
from django.contrib.auth.decorators import user_passes_test
from apps.series.views import *
from django.contrib import messages
from django.db import IntegrityError
# Create your views here.
@login_required
def dashboard(request):
    
    epanimes = (
        EpisodeAnime.objects
        .filter(userepisodeanime__user_id=request.user.id)
        .order_by('-userepisodeanime__date_watched')
        .values('season__anime__id','pt_title', 'number', 'userepisodeanime__date_watched', 'season__number', 'season__anime__or_title')
    )
    movies = (
        Movie.objects
        .filter(usermovie__user_id=request.user.id)
        .order_by('-usermovie__date_watched')
        .values('pt_title','year', 'usermovie__date_watched')
    )
    epseries = (
        EpisodeSerie.objects
        .filter(userepisodeserie__user_id=request.user.id)
        .order_by('-userepisodeserie__date_watched')
        .values('season__serie__id','pt_title', 'number', 'userepisodeserie__date_watched', 'season__number', 'season__serie__or_title')
    )
    books = (
        Book.objects
        .filter(userbook__user_id=request.user.id)
        .order_by('-userbook__date_watched')
        .values('pt_title', 'year', 'userbook__date_watched')
    )
    capmangas = (
        ChapterManga.objects
        .filter(userchaptermanga__user_id=request.user.id)
        .order_by('-userchaptermanga__date_watched')
        .values('volume__manga__id','pt_title', 'number', 'userchaptermanga__date_watched', 'volume__number', 'volume__manga__or_title')
    )
    #preciso ordernar pela data assistida
    for x in books:
        x['date_watched'] = x.pop('userbook__date_watched')
        x['type'] = 'Livro'
    for x in epanimes:
        x['date_watched'] = x.pop('userepisodeanime__date_watched')
        x['type'] = 'Anime'
    for x in movies:
        x['date_watched'] = x.pop('usermovie__date_watched')
        x['type'] = 'Filme'
    for x in epseries:
        x['date_watched'] = x.pop('userepisodeserie__date_watched')
        x['type'] = 'Série'
    for x in capmangas:
        x['date_watched'] = x.pop('userchaptermanga__date_watched')
        x['type'] = 'Mangá'
    
    todos = list(chain(epanimes, movies, epseries, books, capmangas))

    # Define uma função para obter a data assistida de um dicionário
    def get_date_watched(item):
        return item.get('date_watched', None)  # Retorna None se a chave não existir

    sorted_todos = sorted(todos, key=get_date_watched, reverse=True)[:25]
    
    context = {
        'all': sorted_todos
    }
    template_name = 'dashboard.html'
    return render(request, template_name, context)

def register(request):
    template_name = 'register.html'
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=user.username, password=form.cleaned_data['password1'])
            login(request, user)
            return redirect('core:home')
    else:
        form = RegisterForm()
    context = {
        'form': form
    }
    return render(request, template_name, context)

@login_required
def edit(request):
    template_name = 'edit.html'
    context = {}
    if request.method == 'POST': #Se o método for POST
        form = EditAccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            form = EditAccountForm(instance=request.user)
            context['success'] = True
            #return redirect ('app_accounts:dashboard')
    else:
        form = EditAccountForm(instance=request.user)
    context['form'] = form
    return render(request,template_name, context)

@login_required
def edit_password(request):
    template_name = 'edit_password.html'
    context = {}
    if request.method == 'POST': #Se o método for POST
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            context['success'] = True
            
    else:
        form = PasswordChangeForm(user=request.user)
    context['form'] = form
    return render(request, template_name, context)

@login_required
def DashboardSeries(request):
    context = {}
    qtd_assistidos = UserEpisodeSerie.objects.filter(user=request.user).count()
    epseries = (
        EpisodeSerie.objects
        .filter(userepisodeserie__user_id=request.user.id)
        .order_by('-userepisodeserie__date_watched')
        .values('pt_title', 'number', 'userepisodeserie__date_watched', 'season__number', 'season__serie__or_title')[:10]
    )
    
    context = {
        'total_assistidos': qtd_assistidos,
        'epseries': epseries,
        'qtd_assistidos': epseries.count
        
    }
    template_name = 'DashboardSeries.html'
    return render(request, template_name, context)

@login_required
def DashboardAnimes(request):
    context = {}
    qtd_assistidos = UserEpisodeAnime.objects.filter(user=request.user).count()
    epanimes = (
        EpisodeAnime.objects
        .filter(userepisodeanime__user_id=request.user.id)
        .order_by('-userepisodeanime__date_watched')
        .values('pt_title', 'number', 'userepisodeanime__date_watched', 'season__number', 'season__anime__or_title')[:10]
    )
    context = {
        'qtd_assistidos': epanimes.count,
        'epanimes': epanimes,
        'qtd_total': qtd_assistidos
    }
    template_name = 'DashboardAnimes.html'
    return render(request, template_name, context)

@login_required
def DashboardMovies(request):
    context = {}
    qtd_assistidos = UserMovie.objects.filter(user=request.user).count()
    movies = (
        Movie.objects
        .filter(usermovie__user_id=request.user.id)
        .order_by('-usermovie__date_watched')
        .values('pt_title', 'usermovie__date_watched')[:10]
    )

    context = {
        'total_assistidos': qtd_assistidos,
        'movies': movies,
        'qtd_assistidos': movies.count
    }
    template_name = 'DashboardMovies.html'
    return render(request, template_name, context)

@login_required
def DashboardMangas(request):
    context = {}
    qtd_lidos = UserChapterManga.objects.filter(user=request.user).count()
    capmangas = (
        ChapterManga.objects
        .filter(userchaptermanga__user_id=request.user.id)
        .order_by('-userchaptermanga__date_watched')
        .values('pt_title', 'number', 'userchaptermanga__date_watched', 'volume__number', 'volume__manga__or_title')[:10]
    )
    context = {
        'total_lidos': qtd_lidos,
        'capmangas': capmangas,
        'qtd_lidos': capmangas.count
    }
    template_name = 'DashboardMangas.html'
    return render(request, template_name, context)

@login_required
def DashboardBooks(request):
    context = {}
    qtd_lidos = UserBook.objects.filter(user=request.user).count()
    books = (
        Book.objects
        .filter(userbook__user_id=request.user.id)
        .order_by('-userbook__date_watched')
        .values('pt_title', 'userbook__date_watched')[:10]
    )

    context = {
        'total_lidos': qtd_lidos,
        'qtd_lidos': books.count,
        'books': books,
        
    }
    template_name = 'DashboardBooks.html'
    return render(request, template_name, context)

@login_required
def DashboardFavorites(request):
    context = {}
      
    todos = FavoritesView.objects.filter(user=request.user.id)
    todos_objetos = []
    for x in todos:
        if x.type == 'Anime':
            b = FavoriteAnime.objects.filter(anime_id = x.conteudo_id).first().anime
            b.percentual = percentual_lido_anime(request=request, anime=b)
            b.type = x.type
            todos_objetos.append(b)
        elif x.type == 'Mangá':
            b = FavoriteManga.objects.filter(manga_id = x.conteudo_id).first().manga
            b.percentual = percentual_lido_manga(request=request, manga=b)
            b.type = x.type
            todos_objetos.append(b)
        elif x.type == 'Série':
            b = FavoriteSerie.objects.filter(serie_id = x.conteudo_id).first().serie
            b.percentual = percentual_lido_serie(request=request, serie=b)
            b.type = x.type
            todos_objetos.append(b)
        elif x.type == 'Livro':
            b = FavoriteBook.objects.filter(book_id = x.conteudo_id).first().book
            b.percentual = 100
            b.type = x.type
            todos_objetos.append(b)
        elif x.type == 'Filme':
            b = FavoriteMovie.objects.filter(movie_id = x.conteudo_id).first().movie
            b.percentual = 100
            b.type = x.type
            todos_objetos.append(b)
   
    context = {
        'qtd_favorites': todos_objetos.count,
        'favorites': todos_objetos,
    }
    
    template_name = 'DashboardFavorites.html'
    return render(request, template_name, context)

@login_required
def percentual_lido_manga(request, manga):
    qtd_chapters = 0
    qtd_chapters_watched = 0
    mangasvolume = VolumeManga.objects.filter(manga_id=manga.id)
    for volume in mangasvolume:
        volumechapters = ChapterManga.objects.filter(volume_id = volume.id)
        volumechapters_watched = UserChapterManga.objects.filter(chapter__volume_id = volume.id, user=request.user)
        qtd_chapters += volumechapters.count()
        qtd_chapters_watched += volumechapters_watched.count()
    #print(f"Mangá: {manga.or_title}\nQuantidade: {qtd_chapters_watched}/{qtd_chapters} = {qtd_chapters_watched/qtd_chapters*100:.2f}%")
    percentual = (qtd_chapters_watched/qtd_chapters*100)
    return percentual

@login_required
def percentual_lido_anime(request, anime):
    qtd_episodesanime = 0
    qtd_episodes_anime_watched = 0
    animesseason = SeasonAnime.objects.filter(anime_id=anime.id)
    for season in animesseason:
        seasonepisodes = EpisodeAnime.objects.filter(season_id = season.id)
        seasonepisodes_watched = UserEpisodeAnime.objects.filter(episode__season_id = season.id, user=request.user)
        qtd_episodesanime += seasonepisodes.count()
        qtd_episodes_anime_watched += seasonepisodes_watched.count()
    #print(f"Mangá: {manga.or_title}\nQuantidade: {qtd_chapters_watched}/{qtd_chapters} = {qtd_chapters_watched/qtd_chapters*100:.2f}%")
    percentual = (qtd_episodes_anime_watched/qtd_episodesanime*100)
    return percentual

@login_required
def percentual_lido_serie(request, serie):
    qtd_episodesserie = 0
    qtd_episodes_serie_watched = 0
    seriesseason = SeasonSerie.objects.filter(serie_id=serie.id)
    for season in seriesseason:
        seasonepisodes = EpisodeSerie.objects.filter(season_id = season.id)
        seasonepisodes_watched = UserEpisodeSerie.objects.filter(episode__season_id = season.id, user=request.user)
        qtd_episodesserie += seasonepisodes.count()
        qtd_episodes_serie_watched += seasonepisodes_watched.count()
    #print(f"Mangá: {manga.or_title}\nQuantidade: {qtd_chapters_watched}/{qtd_chapters} = {qtd_chapters_watched/qtd_chapters*100:.2f}%")
    percentual = (qtd_episodes_serie_watched/qtd_episodesserie*100)
    return percentual

def RemoverFavorito(request, id, type):
    if type == 'Anime':
        temp = FavoriteAnime.objects.get(anime_id=id, user=request.user)
        print(temp)
    if type == 'Livro':
        temp = FavoriteBook.objects.get(book_id=id, user=request.user)
    if type == 'Mangá':
        temp = FavoriteManga.objects.get(manga_id=id, user=request.user)
    if type == 'Filme':
        temp = FavoriteMovie.objects.get(movie_id=id, user=request.user)
    if type == 'Série':
        temp = FavoriteSerie.objects.get(serie_id=id, user=request.user)
        
    if (temp):
        temp.delete()
        return redirect('accounts:DashboardFavorites')
    else:
        return redirect('accounts:DashboardFavorites')

@user_passes_test(lambda u: u.is_staff)
def DashboardManager(request):
    
    context = {
        
    }
    template_name = 'DashboardManager.html'

    return render(request, template_name, context)
   
@user_passes_test(lambda u: u.is_staff)
def DashboardAddSerie(request):
    if request.method == 'POST':
        if 'submit_serie' in request.POST:
            form_serie = AdicionarSerieForm(request.POST)
            if form_serie.is_valid():
                nome_da_serie = form_serie.cleaned_data['or_title']
                if Serie.objects.filter(or_title=nome_da_serie).first():
                    messages.error(request, 'Erro ao adicionar série.')
                    return redirect('accounts:DashboardAddSerie')
                else:
                    form_serie.save()
                    messages.success(request, 'Série adicionada com sucesso.')
                return redirect('accounts:DashboardAddSerie')
            else:
                messages.error(request, 'Erro ao adicionar série.')
                return redirect('accounts:DashboardAddSerie')
        elif 'submit_season' in request.POST:
            form_seasonserie = AdicionarSeasonSerieForm(request.POST)
            if form_seasonserie.is_valid():
                form_seasonserie.save()
                messages.success(request, 'Temporada adicionada com sucesso.')
                return redirect('accounts:DashboardAddSerie')
            else:
                messages.error(request, 'Erro ao adicionar temporada.')
                return redirect('accounts:DashboardAddSerie')
        elif 'submit_episode' in request.POST:
            form_episodeserie = AdicionarEpisodeSerieForm(request.POST)
            if form_episodeserie.is_valid():
                form_episodeserie.save()
                messages.success(request, 'Episódio adicionado com sucesso.')
                return redirect('accounts:DashboardAddSerie')
            else:
                messages.error(request, 'Erro ao adicionar episódio.')
                return redirect('accounts:DashboardAddSerie')
    else:
        form_serie = AdicionarSerieForm()
        form_seasonserie = AdicionarSeasonSerieForm()
        form_episodeserie = AdicionarEpisodeSerieForm()

    context = {
        'form_serie': form_serie,
        'form_seasonserie': form_seasonserie,
        'form_episodeserie': form_episodeserie
    }
    template_name = 'DashboardAddSerie.html'
    return render(request, template_name, context)

@user_passes_test(lambda u: u.is_staff)
def DashboardAddSerieCompleta(request):
    if request.method == 'POST':
        form = AdicionarSerieCompletaForm(request.POST)
        if form.is_valid():
            serie_id = form.cleaned_data['serie']
            season_number = form.cleaned_data['season_number']
            qtd_eps = form.cleaned_data['qtd_eps']
            try:
                # Tenta criar a temporada
                season_temporaria = SeasonSerie(number=season_number, serie_id=serie_id)
                season_temporaria.save()
                season_temporaria.insert_eps(qtd_eps=qtd_eps)
                messages.success(request, 'Temporada adicionada com sucesso.')
            except IntegrityError:
                # Se a temporada já existe, exibe uma mensagem de erro
                messages.error(request, 'Já existe uma temporada com este número e série.')

            return redirect('accounts:DashboardAddSerieCompleta')
        else:
            form = AdicionarSerieCompletaForm()
    else:
        form = AdicionarSerieCompletaForm()

    context = {
        'form': form,
        }
    template_name = 'DashboardAddSerieCompleta.html'

    return render(request, template_name, context)

@user_passes_test(lambda u: u.is_staff)
def DashboardAddAnime(request):
    if request.method == 'POST':
        if 'submit_anime' in request.POST:
            form_anime = AdicionarAnimeForm(request.POST)
            if form_anime.is_valid():
                nome_do_anime = form_anime.cleaned_data['or_title']
                if Serie.objects.filter(or_title=nome_do_anime).first():
                    messages.error(request, 'Erro ao adicionar anime.')
                    return redirect('accounts:DashboardAddAnime')
                else:
                    form_anime.save()
                    messages.success(request, 'Anime adicionada com sucesso.')
                return redirect('accounts:DashboardAddAnime')
            else:
                messages.error(request, 'Erro ao adicionar Anime.')
                return redirect('accounts:DashboardAddAnime')
        elif 'submit_season' in request.POST:
            form_seasonanime = AdicionarSeasonAnimeForm(request.POST)
            if form_seasonanime.is_valid():
                form_seasonanime.save()
                messages.success(request, 'Temporada adicionada com sucesso.')
                return redirect('accounts:DashboardAddAnime')
            else:
                messages.error(request, 'Erro ao adicionar temporada.')
                return redirect('accounts:DashboardAddAnime')
        elif 'submit_episode' in request.POST:
            form_episodeanime = AdicionarEpisodeAnimeForm(request.POST)
            if form_episodeanime.is_valid():
                form_episodeanime.save()
                messages.success(request, 'Episódio adicionado com sucesso.')
                return redirect('accounts:DashboardAddAnime')
            else:
                messages.error(request, 'Erro ao adicionar episódio.')
                return redirect('accounts:DashboardAddAnime')
    else:
        form_anime = AdicionarAnimeForm()
        form_seasonanime = AdicionarSeasonAnimeForm()
        form_episodeanime = AdicionarEpisodeAnimeForm()

    context = {
        'form_anime': form_anime,
        'form_seasonanime': form_seasonanime,
        'form_episodeanime': form_episodeanime
    }
    template_name = 'DashboardAddAnime.html'
    return render(request, template_name, context)

@user_passes_test(lambda u: u.is_staff)
def DashboardAddAnimeCompleto(request):
    
    if request.method == 'POST':
        form = AdicionarAnimeCompletoForm(request.POST)
        if form.is_valid():
            anime_id = form.cleaned_data['anime']
            season_number = form.cleaned_data['season_number']
            qtd_eps = form.cleaned_data['qtd_eps']
            ep_inicial = form.cleaned_data['ep_inicial']
        
            try:
                # Tenta criar a temporada
                season_temporaria = SeasonAnime(number=season_number, anime_id=anime_id)
                season_temporaria.save()
                season_temporaria.insert_eps(qtd_eps=qtd_eps, number_ep=ep_inicial)
                messages.success(request, 'Temporada adicionada com sucesso.')
            except IntegrityError:
                # Se a temporada já existe, exibe uma mensagem de erro
                season_temporaria = SeasonAnime.objects.get(number=season_number, anime_id=anime_id)
                season_temporaria.insert_eps(qtd_eps=qtd_eps, number_ep=ep_inicial)
                messages.error(request, 'Já existe uma temporada com este número e anime. Porém, adicionamos os episódios')

            return redirect('accounts:DashboardAddAnimeCompleto')
        else:
            form = AdicionarAnimeCompletoForm()
    else:
        form = AdicionarAnimeCompletoForm()

    context = {
        'form': form
    }
    template_name = 'DashboardAddAnimeCompleto.html'

    return render(request, template_name, context)

@user_passes_test(lambda u: u.is_staff)
def DashboardAddManga(request):
    
    if request.method == 'POST':
        if 'submit_manga' in request.POST:
            form_manga = AdicionarMangaForm(request.POST)
            if form_manga.is_valid():
                manga_name = form_manga.cleaned_data['or_title']
                if Manga.objects.filter(or_title=manga_name).first():
                    messages.error(request, 'Erro ao adicionar mangá.')
                    return redirect('accounts:DashboardAddManga')
                else:
                    form_manga.save()
                    messages.success(request, 'Mangá adicionado com sucesso.')
                return redirect('accounts:DashboardAddManga')
            else:
                messages.error(request, 'Erro ao adicionar Mangá.')
                return redirect('accounts:DashboardAddManga')
        elif 'submit_volume' in request.POST:
            form_volumemanga = AdicionarVolumeMangaForm(request.POST)
            if form_volumemanga.is_valid():
                form_volumemanga.save()
                messages.success(request, 'Volume adicionada com sucesso.')
                return redirect('accounts:DashboardAddManga')
            else:
                messages.error(request, 'Erro ao adicionar volume.')
                return redirect('accounts:DashboardAddManga')
        elif 'submit_chapter' in request.POST:
            form_chaptermanga = AdicionarChapterMangaForm(request.POST)
            if form_chaptermanga.is_valid():
                form_chaptermanga.save()
                messages.success(request, 'Capítulo adicionado com sucesso.')
                return redirect('accounts:DashboardAddManga')
            else:
                messages.error(request, 'Erro ao adicionar capítulo.')
                return redirect('accounts:DashboardAddManga')
    else:
        form_manga = AdicionarMangaForm()
        form_volumemanga = AdicionarVolumeMangaForm()
        form_chaptermanga = AdicionarChapterMangaForm()

    context = {
        'form_manga': form_manga,
        'form_volumemanga': form_volumemanga,
        'form_chaptermanga': form_chaptermanga
    }
    template_name = 'DashboardAddManga.html'
    return render(request, template_name, context)

@user_passes_test(lambda u: u.is_staff)
def DashboardAddMangaCompleto(request):
    
    if request.method == 'POST':
        form = AdicionarMangaCompletoForm(request.POST)
        if form.is_valid():
            manga_id = form.cleaned_data['manga']
            volume_number = form.cleaned_data['volume_number']
            qtd_caps = form.cleaned_data['qtd_caps']
            cap_inicial = form.cleaned_data['cap_inicial']
        
            try:
                # Tenta criar a temporada
                volume_temporario = VolumeManga(number=volume_number, manga_id=manga_id)
                volume_temporario.save()
                volume_temporario.insert_caps(qtd_caps=qtd_caps, number_cap=cap_inicial)
                messages.success(request, 'Volume adicionado com sucesso.')
            except IntegrityError:
                # Se a temporada já existe, exibe uma mensagem de erro
                volume_temporario = VolumeManga.objects.get(number=volume_number, manga_id=manga_id)
                volume_temporario.insert_caps(qtd_caps=qtd_caps, number_cap=cap_inicial)
                messages.error(request, 'Já existe um volume com este número e mangá. Porém, adicionamos os capítulos')

            return redirect('accounts:DashboardAddMangaCompleto')
        else:
            form = AdicionarMangaCompletoForm()
    else:
        form = AdicionarMangaCompletoForm()

    context = {
        'form': form
    }
    template_name = 'DashboardAddMangaCompleto.html'

    return render(request, template_name, context)

@user_passes_test(lambda u: u.is_staff)
def DashboardAddMovie(request):
    
    context = {
        
    }
    template_name = 'DashboardAddSerie.html'

    return render(request, template_name, context)

@user_passes_test(lambda u: u.is_staff)
def DashboardAddBook(request):
    
    context = {
        
    }
    template_name = 'DashboardAddSerie.html'

    return render(request, template_name, context)

@user_passes_test(lambda u: u.is_staff)
def DashboardRemove(request):
    
    context = {
        
    }
    template_name = 'DashboardRemove.html'

    return render(request, template_name, context)

