from django.shortcuts import render
from .models import Serie
from apps.core.models import Season
# Create your models here.

def series (request):
    context = {}
    series = Serie.objects.all()
    qtd_series = len(series) #Quantidade de series 0-4
    
    
    #qtd = Season.objects.filter(serie_id=series[0]).count() #Quantidade de temporadas da primeira serie

    for serie in series:
        temp_count = Season.objects.filter(serie_id=serie.id).count()
        serie.qtd_temps = temp_count

 
    template_name = 'series.html'
    context['series'] = series
    context['qtd_series'] = qtd_series
    return render(request, template_name, context)