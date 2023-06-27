from django.contrib import admin
from .models import Anime, SeasonAnime, EpisodeAnime

class AnimeAdmin(admin.ModelAdmin):
    list_display = ['or_title', 'pt_title', 'author', 'situation', 'created_at']
    
class SeasonAnimeAdmin(admin.ModelAdmin):
    list_display = ['number', 'pt_title', 'or_title', 'anime']
    
class EpisodeAnimeAdmin(admin.ModelAdmin):
    list_display = ['number', 'pt_title', 'or_title', 'season']

admin.site.register(Anime, AnimeAdmin)
admin.site.register(SeasonAnime, SeasonAnimeAdmin)
admin.site.register(EpisodeAnime, EpisodeAnimeAdmin)
