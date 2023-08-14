from django.contrib import admin
from .models import Serie, SeasonSerie, EpisodeSerie

class SerieAdmin(admin.ModelAdmin):
    list_display = ['or_title','pt_title', 'director', 'situation', 'created_at']
    ordering = ['-created_at']

class SeasonSerieAdmin(admin.ModelAdmin):
    list_display = ['display_number', 'pt_title', 'or_title', 'serie']
    
    def display_number(self, obj): #Substitui a exibição do campo number pelo método abaixo e utiliza esse método no list_display para exibir
        return f"Temporada {obj.number}"
    display_number.short_description = "Temporada" #Cria a descrição curta para exibir no cabeçalho da tabela
    
    
class EpisodeSerieAdmin(admin.ModelAdmin):
    list_display = ['display_number', 'pt_title', 'or_title', 'season']
    search_fields = ['number','or_title', 'season__or_title', 'season__serie__or_title']
    def display_number(self, obj): #Substitui a exibição do campo number pelo método abaixo e utiliza esse método no list_display para exibir
        return f"Episódio {obj.number}"
    display_number.short_description = "Episódio" #Cria a descrição curta para exibir no cabeçalho da tabela
        
admin.site.register(Serie, SerieAdmin)
admin.site.register(SeasonSerie, SeasonSerieAdmin)
admin.site.register(EpisodeSerie, EpisodeSerieAdmin)
