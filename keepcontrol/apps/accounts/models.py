import re
from django.db import models
from django.core import validators
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, UserManager)
from apps.series.models import EpisodeSerie
from apps.animes.models import EpisodeAnime
from apps.movies.models import Movie

class User(AbstractBaseUser, PermissionsMixin):
  
    username = models.CharField('Nome de usuário', max_length=30, unique=True,
                                validators=[
                                    validators.RegexValidator(
                                        re.compile('^[\w.@=-]+$'),
                                        'O nome de usuário só pode contar, letras, digitos ou @/./+/-/_',
                                        'invalid')
                                ]
    )
    email = models.EmailField('E-mail', unique=True)
    name = models.CharField('Nome completo', max_length=100, blank=True)
    is_active = models.BooleanField('Está ativo?', blank=True, default=True)
    is_staff = models.BooleanField('É da equipe', blank=True, default=False)
    date_joined = models.DateTimeField('Data de entrada', auto_now_add=True)
    
    #Conteúdo
    episodes_anime = models.ManyToManyField(EpisodeAnime, through='UserEpisodeAnime', blank=True)
    episodes_serie = models.ManyToManyField(EpisodeSerie, through='UserEpisodeSerie', blank=True)
    movies = models.ManyToManyField(Movie, through='UserMovie', blank=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    def __str__(self):
        return self.name or self.username
    
    def get_short_name(self):
        return self.username
    
    def get_full_name(self):
        return str(self)
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

class UserMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    date_watched = models.DateTimeField()

    def __str__(self):
        return f"Usuário: {self.user.username}, Movie: {self.movie.pt_title}, Assistido em: {self.date_watched}"
    
    class Meta:
        verbose_name = 'Filme do Usuário'
        verbose_name_plural = 'Filmes do Usuário'
        
class UserEpisodeSerie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    episode = models.ForeignKey(EpisodeSerie, on_delete=models.CASCADE)
    date_watched = models.DateTimeField()

    def __str__(self):
        return f"Usuário: {self.user.username}, Episódio: {self.episode.number}, Assistido em: {self.date_watched}"

    class Meta:
        verbose_name = 'Episódio de série do Usuário'
        verbose_name_plural = 'Episódios de séries do Usuário'

class UserEpisodeAnime(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    episode = models.ForeignKey(EpisodeAnime, on_delete=models.CASCADE)
    date_watched = models.DateTimeField()

    def __str__(self):
        return f"Usuário: {self.user.username}, Episódio: {self.episode.number}, Assistido em: {self.date_watched}"

    class Meta:
        verbose_name = 'Episódio de anime do Usuário'
        verbose_name_plural = 'Episódios de animes do Usuário'
    
    
