from django.shortcuts import render
from .models import Movie
# Create your models here.



def movies (request):
    
    movies = Movie.objects.all()
    qtd_movies = len(movies)

    template_name = 'movies.html'
    context = {
        'movies': movies,
        'qtd_movies': qtd_movies
    }

    return render(request, template_name, context)