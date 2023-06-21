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
    
    def get_qtd_seasons(id_da_serie):
        return Season.objects.filter(serie_id=id_da_serie).count() #Número de Temporadas da Série com este ID
    class Meta:
        verbose_name = 'Temporada'
        verbose_name_plural = 'Temporadas'

    def get_seasons(id_da_serie):
        return Season.objects.filter(serie_id=id_da_serie)
    
    def insert_eps(self, qtd_eps):
        cont = 0
        for i in range(qtd_eps):
            nummber_of_ep = i+1
            title_of_episode_for_insert = 'Episódio '+str(nummber_of_ep) 
            id_of_season = self.id
            temp = Episode(title=title_of_episode_for_insert, season_id=id_of_season)
            if Episode.objects.filter(title=temp.title, season_id=temp.season_id).exists():
                print(title_of_episode_for_insert+' já existe')
                #Se o episódio existir, não fazer nada.
            else:
                #Se o episódio não existir, inserir no banco.
                temp.save()
                print(temp.title+' inserido!')
                cont = cont+1
        return 'Número de episódios adicionados: '+str(cont)         
            

class Episode(models.Model):
    title = models.CharField('Episódio', max_length=255)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, blank=True, null=False, verbose_name="Temporada")
    
    def __str__ (self):
        return self.title
    
    def get_qtd_episodes(id):
        return Episode.objects.filter(season_id=id).count() #Número de Episódios da Temporada com este ID
    
    def get_episodes(id_da_season):
        return Episode.objects.filter(season_id=id_da_season)

    class Meta:
        verbose_name = 'Episódio'
        verbose_name_plural = 'Episódios'

    