from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.conf import settings
from .forms import RegisterForm, EditAccountForm
from apps.movies.models import Movie
from apps.series.models import EpisodeSerie, Serie
from apps.animes.models import EpisodeAnime, Anime
from apps.mangas.models import ChapterManga, Manga
from apps.books.models import Book
from .models import UserEpisodeAnime, UserEpisodeSerie, UserMovie, UserChapterManga, UserBook
from itertools import chain
# Create your views here.
@login_required
def dashboard(request):
    
    epanimes = (
        EpisodeAnime.objects
        .filter(userepisodeanime__user_id=request.user.id)
        .order_by('-userepisodeanime__date_watched')
        .values('pt_title', 'number', 'userepisodeanime__date_watched', 'season__number', 'season__anime__or_title')[:10]
    )
    movies = (
        Movie.objects
        .filter(usermovie__user_id=request.user.id)
        .order_by('-usermovie__date_watched')
        .values('pt_title','year', 'usermovie__date_watched')[:10]
    )
    epseries = (
        EpisodeSerie.objects
        .filter(userepisodeserie__user_id=request.user.id)
        .order_by('-userepisodeserie__date_watched')
        .values('pt_title', 'number', 'userepisodeserie__date_watched', 'season__number', 'season__serie__or_title')[:5]
    )
    books = (
        Book.objects
        .filter(userbook__user_id=request.user.id)
        .order_by('-userbook__date_watched')
        .values('pt_title', 'year', 'userbook__date_watched')[:10]
    )
    capmangas = (
        ChapterManga.objects
        .filter(userchaptermanga__user_id=request.user.id)
        .order_by('-userchaptermanga__date_watched')
        .values('pt_title', 'number', 'userchaptermanga__date_watched', 'volume__number', 'volume__manga__or_title')[:10]
    )
    
    todos = list(chain(epanimes,movies,epseries,books,capmangas))
        
    #preciso ordernar pela data assistida
                
    context = {
        'all': todos
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
        'qtd_assistidos': qtd_assistidos,
        'epseries': epseries,
        
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
        'epanimes': epanimes,
        'qtd_assistidos': qtd_assistidos,
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