from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.conf import settings
from .forms import RegisterForm, EditAccountForm
from apps.movies.models import Movie
from apps.series.models import EpisodeSerie, Serie, SeasonSerie
from apps.animes.models import EpisodeAnime, Anime, SeasonAnime
from apps.mangas.models import ChapterManga, Manga, VolumeManga
from apps.books.models import Book
from .models import UserEpisodeAnime, UserEpisodeSerie, UserMovie, UserChapterManga, UserBook, FavoriteManga, FavoriteAnime, FavoriteBook, FavoriteMovie, FavoriteSerie
from itertools import chain
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
    mangas = []
    animes = []
    series = []
    books = []
    movies = []
    all = []
    
    favorites_mangas = FavoriteManga.objects.filter(user=request.user.id)
    favorites_animes = FavoriteAnime.objects.filter(user=request.user.id)
    favorites_series = FavoriteSerie.objects.filter(user=request.user.id)
    favorites_books = FavoriteBook.objects.filter(user=request.user.id)
    favorites_movies = FavoriteMovie.objects.filter(user=request.user.id)
    
    # ------ Tratamento Mangás ----- #
    for item in favorites_mangas:
        print(item)
        mangas.append(item.manga)
    
    for favorite in mangas:
        favorite.percentual = percentual_lido(request=request, manga=favorite)
        
    for item in mangas:
        all.append(item)
    # -------- Tratamento Animes ------------------#
    
    for item in favorites_animes:
        print(item)
        animes.append(item.anime)
    
    for item in animes:
        all.append(item)
    
     # -------- Tratamento series ------------------#
    
    for item in favorites_series:
        print(item)
        series.append(item.serie)
    
    for item in series:
        all.append(item)
        
    # -------- Tratamento Livros ------------------#
    
    for item in favorites_books:
        print(item)
        books.append(item.book)
    
    for item in books:
        all.append(item)
        
    # -------- Tratamento Filmes ------------------#
    
    for item in favorites_movies:
        print(item)
        movies.append(item.movie)
    
    for item in movies:
        all.append(item)
    
    # -----------------------------------------------#
    context = {
        'qtd_favorites': mangas.count,
        'favorites': all,
    }
    
    template_name = 'DashboardFavorites.html'
    return render(request, template_name, context)

@login_required
def percentual_lido(request, manga):
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