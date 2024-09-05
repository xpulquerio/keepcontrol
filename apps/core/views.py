from django.shortcuts import render
from apps.animes.models import Anime
from apps.series.models import Serie
from apps.movies.models import Movie
from apps.books.models import Book
from apps.mangas.models import Manga
from itertools import chain
# Create your views here.

def home (request):
    context = {}
    animes = Anime.objects.all().order_by('-created_at')[:5]
    movies = Movie.objects.all().order_by('-created_at')[:5]
    series = Serie.objects.all().order_by('-created_at')[:5]
    books = Book.objects.all().order_by('-created_at')[:5]
    mangas = Manga.objects.all().order_by('-created_at')[:5]

    for x in animes:
        x.type = 'Anime'
    for x in series:
        x.type = 'Série'
    for x in movies:
        x.type = 'Filme'
    for x in books:
        x.type = 'Livro'
    for x in mangas:
        x.type = 'Mangá'
    
    todos = list(chain(animes,movies,series,books,mangas))
        
    todos_ordenados = sorted(todos, key=lambda x: x.created_at, reverse=True)
    
    template_name = 'home.html'
    context['all'] = todos_ordenados

    return render(request, template_name, context)