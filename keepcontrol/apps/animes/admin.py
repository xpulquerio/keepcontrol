from django.contrib import admin
from .models import Anime, SeasonAnime, EpisodeAnime

class AnimeAdmin(admin.ModelAdmin):
    list_display = ['or_title', 'pt_title', 'author', 'situation', 'created_at']
    
class SeasonAnimeAdmin(admin.ModelAdmin):
    list_display = ['display_number', 'pt_title', 'or_title', 'anime']
    def display_number(self, obj): #Substitui a exibição do campo number pelo método abaixo e utiliza esse método no list_display para exibir
        return f"Temporada {obj.number}"
    display_number.short_description = "Temporada" #Cria a descrição curta para exibir no cabeçalho da tabela
    
class EpisodeAnimeAdmin(admin.ModelAdmin):
    list_display = ['display_number', 'pt_title', 'or_title', 'season']
    def display_number(self, obj): #Substitui a exibição do campo number pelo método abaixo e utiliza esse método no list_display para exibir
        return f"Episódio {obj.number}"
    display_number.short_description = "Episódio" #Cria a descrição curta para exibir no cabeçalho da tabela

admin.site.register(Anime, AnimeAdmin)
admin.site.register(SeasonAnime, SeasonAnimeAdmin)
admin.site.register(EpisodeAnime, EpisodeAnimeAdmin)
