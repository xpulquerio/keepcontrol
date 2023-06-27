from django.shortcuts import render
from .models import Movie
# Create your models here.


def movies (request):
    
    movies = Movie.objects.all().order_by('-year')
    
    qtd_movies = len(movies)

    usuario = request.user
    
    for movie in movies:
        user_movie = movie.usermovie_set.filter(user=usuario.id).first()
        if user_movie and user_movie.date_watched:
            movie.assist = user_movie.date_watched
        movies.order_by('usermovie')        
    
    
    template_name = 'movies.html'
    context = {
        'movies': movies,
        'qtd_movies': qtd_movies
    }

    return render(request, template_name, context)