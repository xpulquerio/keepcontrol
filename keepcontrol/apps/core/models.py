from django.db import models
from apps.series.models import Serie

# Create your models here.
class Season(models.Model):
    title = models.CharField('Temporada', max_length=255)
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE, blank=True, null=False, verbose_name="Série")
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__ (self):
        return self.title
    
    def get_qtd_seasons(id):
        return Season.objects.filter(serie_id=id).count() #Número de Temporadas da Série com este ID
    class Meta:
        verbose_name = 'Temporada'
        verbose_name_plural = 'Temporadas'

class Episode(models.Model):
    title = models.CharField('Episódio', max_length=255)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, blank=True, null=False, verbose_name="Temporada")
    
    def __str__ (self):
        return self.title
    
    def get_qtd_episodes(id):
        return Episode.objects.filter(season_id=id).count() #Número de Episódios da Temporada com este ID
    class Meta:
        verbose_name = 'Episódio'
        verbose_name_plural = 'Episódios'

    