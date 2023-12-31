from django.shortcuts import render, redirect
from .models import Movie
from apps.accounts.models import UserMovie
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
# Create your models here.

def ListMovie(request):
    
    search_query = request.GET.get('search')
    
    if search_query:
        movies = Movie.objects.search(search_query)
        movies = Movie.objects.filter(
            Q(pt_title__icontains=search_query) |  # Busca por título em português (case-insensitive)
            Q(or_title__icontains=search_query)    # Busca por título em inglês (case-insensitive)
        ).order_by('pt_title')
    else:
        movies = Movie.objects.all().order_by('collection', '-created_at')
    
    usuario = request.user
    
    for movie in movies:
        user_movie = movie.usermovie_set.filter(user=usuario.id).first()
        if user_movie and user_movie.date_watched:
            movie.date_watched = user_movie.date_watched
    
    movies_paginator = Paginator(movies, 20)
    
    page_num = request.GET.get('page')
   
    page = movies_paginator.get_page(page_num)
    
    template_name = 'movies.html'
    context = {
        'page': page,
        #'qtd_movies': movies.count()
        'qtd_movies': movies_paginator.count,
        'qtd_pages': movies_paginator.num_pages,
        'search_query': search_query  # Passar o valor de busca para o template
    }

    return render(request, template_name, context)

@login_required
def inserir_assistido(request, filme_id):
    usuario = request.user
    movie_user = UserMovie.objects.filter(user=usuario.id, movie=filme_id)
    if movie_user:
        print (str(movie_user)+" já foi assistido pelo usuário")
        return redirect('movies:ListMovie')
    else:
        m = Movie.objects.filter(id=filme_id).first()
        x = UserMovie(movie=m, user=usuario, date_watched=timezone.now()) #Depois alterar o banco para inserir a data automaticamente
        x.save()
        print (str(x)+" inserido!")
        return redirect('movies:ListMovie')