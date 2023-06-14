from django.shortcuts import render

# Create your views here.

def series (request):
    return render (request, 'series.html')