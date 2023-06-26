from django.shortcuts import render
from .models import Movie
# Create your models here.


def movies (request):
    
    movies = Movie.objects.all()
    qtd_movies = len(movies)

    usuario = request.user
    
    for ep in movies:
        user_movie = ep.usermovie_set.filter(user=usuario.id).first()
        if user_movie and user_movie.date_watched:
            ep.assist = user_movie.date_watched

    template_name = 'movies.html'
    context = {
        'movies': movies,
        'qtd_movies': qtd_movies
    }

    return render(request, template_name, context)