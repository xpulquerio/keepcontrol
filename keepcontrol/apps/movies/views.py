from django.shortcuts import render, redirect
from .models import Movie
from apps.core.models import UserMovie
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your models here.

def movies (request):
    
    movies = Movie.objects.all().order_by('-year')
    
    qtd_movies = len(movies)

    usuario = request.user
    
    for movie in movies:
        user_movie = movie.usermovie_set.filter(user=usuario.id).first()
        if user_movie and user_movie.date_watched:
            movie.date_watched = user_movie.date_watched 
    
    template_name = 'movies.html'
    context = {
        'movies': movies,
        'qtd_movies': qtd_movies
    }

    return render(request, template_name, context)

@login_required
def inserir_assistido(request, filme_id):
    usuario = request.user
    movie_user = UserMovie.objects.filter(user=usuario.id, movie=filme_id)
    if movie_user:
        print (str(movie_user)+" já foi assistido pelo usuário")
        return redirect('movies:movies')
    else:
        m = Movie.objects.filter(id=filme_id).first()
        x = UserMovie(movie=m, user=usuario, date_watched=timezone.now()) #Depois alterar o banco para inserir a data automaticamente
        x.save()
        print (str(x)+" inserido!")
        return redirect('movies:movies')