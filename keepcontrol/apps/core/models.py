from django.db import models
from apps.series.models import Serie
from apps.movies.models import Movie



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
        
    def get_seasons(id_da_serie):
        return Season.objects.filter(serie_id=id_da_serie)
    
    def get_absolute_url(self):
        return '/series/'+ str(self.serie_id)+'/'+ str(self.id) #retorna a URL do curso
    
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
    
    class Meta:
        verbose_name = 'Temporada'
        verbose_name_plural = 'Temporadas'
            

class Episode(models.Model):
    title = models.CharField('Episódio', max_length=255)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, blank=True, null=False, verbose_name="Temporada")
    
    def __str__ (self):
        return f"{self.title} {self.season.title} {self.season.serie.title}"
    
    def get_qtd_episodes(id):
        return Episode.objects.filter(season_id=id).count() #Número de Episódios da Temporada com este ID
    
    def get_episodes(self, id_da_season):
        return Episode.objects.filter(season_id=id_da_season)
    
    def get_date_w (self, user_id):
        return str(UserEpisode.objects.filter(episode=self.id, user=user_id).first().date_watched)

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
        return f"User: {self.user.username}, Episode: {self.episode.title}, Date Watched: {self.date_watched}"

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
        return f"User: {self.user.username}, Movie: {self.movie.title}, Date Watched: {self.date_watched}"
    
    class Meta:
        verbose_name = 'Filme do Usuário'
        verbose_name_plural = 'Filmes do Usuário'