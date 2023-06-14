from django.shortcuts import render
from .models import Movies

# Create your views here.

def movies (request):
    movies = Movies.objects.all()
    template_name = 'movies.html'
    context = {
        'movies': movies
    }
    return render(request, template_name, context)