from django.shortcuts import render

# Create your views here.

def movies (request):
    return render (request, 'movies.html')