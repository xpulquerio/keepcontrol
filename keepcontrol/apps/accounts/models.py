import re
from django.db import models
from django.core import validators
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, UserManager)
from apps.movies.models import Movie
from apps.core.models import Episode
# from books.models import Book

class User (AbstractBaseUser, PermissionsMixin):
  
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
    episodes = models.ManyToManyField(Episode, through='core.UserEpisode', blank=True)
    movies = models.ManyToManyField(Movie, through='core.UserMovie', blank=True)
    # chapters = models.ManyToManyField(Chapter)
    # books = models.ManyToManyField(Book)
    
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
    
