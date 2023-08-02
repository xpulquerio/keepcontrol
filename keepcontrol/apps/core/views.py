from django.shortcuts import render
from apps.animes.models import Anime
from apps.series.models import Serie
from apps.movies.models import Movie
from itertools import chain
# Create your views here.

def home (request):
    context = {}
    animes = Anime.objects.all().order_by('-created_at')[:10]
    movies = Movie.objects.all().order_by('-created_at')[:10]
    series = Serie.objects.all().order_by('-created_at')[:10]
    for x in animes:
        x.type = 'Anime'
    for x in series:
        x.type = 'Série'
    for x in movies:
        x.type = 'Filme'
    
    todos = list(chain(animes,movies,series))
        
    todos_ordenados = sorted(todos, key=lambda x: x.created_at, reverse=True)
    
    template_name = 'home.html'
    context['all'] = todos_ordenados

    return render(request, template_name, context)