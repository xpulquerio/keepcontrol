from django.shortcuts import render

# Create your views here.

def mangas (request):
    return render (request, 'mangas.html')