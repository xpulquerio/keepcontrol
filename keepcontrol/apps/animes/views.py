from django.shortcuts import render

# Create your views here.

def animes (request):
    return render (request, 'animes.html')