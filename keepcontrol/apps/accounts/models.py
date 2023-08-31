import re
from django.db import models
from django.core import validators
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, UserManager)
from apps.series.models import EpisodeSerie, Serie
from apps.animes.models import EpisodeAnime, Anime
from apps.movies.models import Movie
from apps.books.models import Book
from apps.mangas.models import ChapterManga, Manga

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
    chapters_manga = models.ManyToManyField(ChapterManga, through='UserChapterManga', blank=True)
    books = models.ManyToManyField(Book, through='UserBook', blank=True)
    
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='Filme')
    date_watched = models.DateTimeField('Assistido em')

    def __str__(self):
        return f"Usuário: {self.user.username}, Movie: {self.movie.pt_title}, Assistido em: {self.date_watched}"
    
    class Meta:
        verbose_name = 'Filme do Usuário'
        verbose_name_plural = 'Filmes'
        unique_together = ('user', 'movie')
        
class UserEpisodeSerie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    episode = models.ForeignKey(EpisodeSerie, on_delete=models.CASCADE, verbose_name='Episódio')
    date_watched = models.DateTimeField('Assistido em')

    def __str__(self):
        return f"Usuário: {self.user.username}, Episódio: {self.episode.number}, Assistido em: {self.date_watched}"

    class Meta:
        verbose_name = 'Episódio de série'
        verbose_name_plural = 'Episódios de séries'
        unique_together = ('user', 'episode')

class UserEpisodeAnime(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    episode = models.ForeignKey(EpisodeAnime, on_delete=models.CASCADE, verbose_name='Episódio')
    date_watched = models.DateTimeField('Assistido em')

    def __str__(self):
        return f"Usuário: {self.user.username}, Episódio: {self.episode.number}, Assistido em: {self.date_watched}"

    class Meta:
        verbose_name = 'Episódio de anime'
        verbose_name_plural = 'Episódios de animes'
        unique_together = ('user', 'episode')
        
class UserChapterManga(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    chapter = models.ForeignKey(ChapterManga, on_delete=models.CASCADE, verbose_name='Capítulo')
    date_watched = models.DateTimeField('Lido em')

    def __str__(self):
        return f"Usuário: {self.user.username}, Capítulo: {self.chapter.number}, Lido em: {self.date_watched}"

    class Meta:
        verbose_name = 'Capítulo de mangá'
        verbose_name_plural = 'Capítulos de mangás'
        unique_together = ('user', 'chapter')

class UserBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Livro')
    date_watched = models.DateTimeField('Lido em')

    def __str__(self):
        return f"Usuário: {self.user.username}, Livro: {self.book.pt_title}, Lido em: {self.date_watched}"
    
    class Meta:
        verbose_name = 'Livro do usuário'
        verbose_name_plural = 'Livros'
        unique_together = ('user', 'book')
        

class FavoriteBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Livro')
    created_at = models.DateTimeField('Cadastrado em', auto_now_add=True)

    def __str__(self):
        return f"Usuário: {self.user.username}, Livro: {self.book.pt_title}, Cadastrado em: {self.created_at}"
    
    class Meta:
        verbose_name = 'Livro favorito'
        verbose_name_plural = 'Livros favoritos'
        unique_together = ('user', 'book')
    
class FavoriteManga(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE, verbose_name='Mangá')
    created_at = models.DateTimeField('Cadastrado em', auto_now_add=True)

    def __str__(self):
        return f"Usuário: {self.user.username}, Livro: {self.manga.or_title}, Cadastrado em: {self.created_at}"
    
    class Meta:
        verbose_name = 'Mangá favorito'
        verbose_name_plural = 'Mangás favoritos'
        unique_together = ('user', 'manga')
    
class FavoriteSerie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE, verbose_name='Série')
    created_at = models.DateTimeField('Cadastrado em', auto_now_add=True)

    def __str__(self):
        return f"Usuário: {self.user.username}, Livro: {self.serie.or_title}, Cadastrado em: {self.created_at}"
    
    class Meta:
        verbose_name = 'Série favorita'
        verbose_name_plural = 'Séries favoritas'
        unique_together = ('user', 'serie')
    
class FavoriteAnime(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, verbose_name='Anime')
    created_at = models.DateTimeField('Cadastrado em', auto_now_add=True)

    def __str__(self):
        return f"Usuário: {self.user.username}, Livro: {self.anime.or_title}, Cadastrado em: {self.created_at}"
    
    class Meta:
        verbose_name = 'Anime favorito'
        verbose_name_plural = 'Animes favoritos'
        unique_together = ('user', 'anime')
    
class FavoriteMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='Filme')
    created_at = models.DateTimeField('Cadastrado em', auto_now_add=True)

    def __str__(self):
        return f"Usuário: {self.user.username}, Livro: {self.movie.or_title}, Cadastrado em: {self.created_at}"
    
    class Meta:
        verbose_name = 'Filme favorito'
        verbose_name_plural = 'Filmes favoritos'
        unique_together = ('user', 'movie')   
    