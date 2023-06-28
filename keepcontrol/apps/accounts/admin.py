from django.contrib import admin
from django.contrib.auth import get_user_model #Para usar o model do nosso usuário
from .models import UserEpisodeAnime, UserEpisodeSerie, UserMovie

User = get_user_model()

class UserAdmin(admin.ModelAdmin):
    list_display = ['username','name','email']
    search_fields = ['name']
    filter_horizontal = ('episodes_anime', 'episodes_serie', 'movies')

admin.site.register(User, UserAdmin)

# ------------ ADMIN DO CONTEÚDO DO USUÁRIO ---------- #

class UserEpisodeSerieAdmin(admin.ModelAdmin):
    list_display = ['user','episode', 'date_watched']
    
class UserEpisodeAnimeAdmin(admin.ModelAdmin):
    list_display = ['user','episode', 'date_watched']
    
class UserMovieAdmin(admin.ModelAdmin):
    list_display = ['user','movie', 'date_watched']

admin.site.register(UserEpisodeSerie, UserEpisodeSerieAdmin)
admin.site.register(UserEpisodeAnime, UserEpisodeAnimeAdmin)
admin.site.register(UserMovie, UserMovieAdmin)

# Register your models here.
