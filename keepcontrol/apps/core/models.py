from django.db import models
from apps.series.models import Serie
from apps.movies.models import Movie

# Create your models here.
class Season(models.Model):
    pt_title = models.CharField('Título brasileiro', max_length=255, blank=True, null=True)
    or_title = models.CharField('Título original', max_length=255, blank=True, null=True)
    number = models.BigIntegerField('Temporada')
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE, verbose_name="Série")

    def __str__ (self):
        return f"{self.pt_title} - {self.serie.pt_title}"
    
    def get_qtd_seasons(id_da_serie):
        return Season.objects.filter(serie_id=id_da_serie).count() #Número de temporadas da série com este ID
        
    def get_seasons(id_da_serie):
        return Season.objects.filter(serie_id=id_da_serie) #As temporaas da série com este ID
    
    def get_absolute_url(self):
        return '/series/'+ str(self.serie_id)+'/'+ str(self.id)
    
    def insert_eps(self, qtd_eps):
        cont = 0
        for i in range(qtd_eps):
            number_of_ep = i+1
            title_of_episode_for_insert = 'Episódio '+str(number_of_ep) 
            id_of_season = self.id
            temp = Episode(number=number_of_ep, season_id=id_of_season)
            if Episode.objects.filter(number=temp.number, season_id=temp.season_id).exists():
                print(title_of_episode_for_insert+' já existe')
                #Se o episódio existir, não fazer nada.
            else:
                #Se o episódio não existir, inserir no banco.
                temp.save()
                print('EP: '+str(temp.number)+' inserido!')
                cont = cont+1
        return 'Número de episódios adicionados: '+str(cont)
    
    def insert_temps(self, qtd_temps, serie_id):
            cont = 0
            for i in range(qtd_temps):
                nummber_of_season = i+1
                title_of_season_for_insert = 'Temporada '+str(nummber_of_season) 
                temp = Season(pt_title=title_of_season_for_insert, serie_id=serie_id)
                if Season.objects.filter(pt_title=temp.pt_title, serie_id=temp.serie_id).exists():
                    print(title_of_season_for_insert+' já existe')
                    #Se a temporada existe, não fazer nada.
                else:
                    #Se a temporada não existe, inserir no banco.
                    temp.save()
                    print(temp.pt_title+' inserida!')
                    cont = cont+1
            return 'Número de temporadas adicionadas: '+str(cont)
    
    class Meta:
        verbose_name = 'Temporada'
        verbose_name_plural = 'Temporadas'
            

class Episode(models.Model):
    pt_title = models.CharField('Título brasileiro', max_length=255, blank=True, null=True)
    or_title = models.CharField('Título original', max_length=255, blank=True, null=True)
    number = models.BigIntegerField('Episódio')
    season = models.ForeignKey(Season, on_delete=models.CASCADE, verbose_name="Temporada")
    
    def __str__ (self):
        return f"EP:{self.number} - {self.season.pt_title} {self.season.serie.pt_title}"
    
    def get_qtd_episodes(id):
        return Episode.objects.filter(season_id=id).count()
    
    def get_episodes(self, id_da_season):
        return Episode.objects.filter(season_id=id_da_season)
    
    def insert_eps(self, qtd_eps, season_id):
        cont = 0
        for i in range(qtd_eps):
            number_of_ep = i+1
            title_of_episode_for_insert = 'Episódio '+str(number_of_ep) 
            temp = Episode(number=number_of_ep, season_id=season_id)
            if Episode.objects.filter(number=temp.number, season_id=temp.season_id).exists():
                print(title_of_episode_for_insert+' já existe')
                #Se o episódio existir, não fazer nada.
            else:
                #Se o episódio não existir, inserir no banco.
                temp.save()
                print('EP: '+str(temp.number)+' inserido!')
                cont = cont+1
        return 'Número de episódios adicionados: '+str(cont)
    
    class Meta:
        verbose_name = 'Episódio'
        verbose_name_plural = 'Episódios'

class UserEpisode(models.Model):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE)
    date_watched = models.DateTimeField()

    def __str__(self):
        return f"Usuário: {self.user.username}, Episódio: {self.episode.number}, Assistido em: {self.date_watched}"

    class Meta:
        verbose_name = 'Episódio do Usuário'
        verbose_name_plural = 'Episódios do Usuário'

class UserMovie(models.Model):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    date_watched = models.DateTimeField()

    def __str__(self):
        return f"Usuário: {self.user.username}, Movie: {self.movie.pt_title}, Assistido em: {self.date_watched}"
    
    class Meta:
        verbose_name = 'Filme do Usuário'
        verbose_name_plural = 'Filmes do Usuário'