from django.contrib import admin
from .models import Serie, SeasonSerie, EpisodeSerie
from apps.accounts.models import UserEpisodeSerie

class SerieAdmin(admin.ModelAdmin):
    list_display = ['or_title','pt_title', 'director', 'situation', 'created_at']

class SeasonSerieAdmin(admin.ModelAdmin):
    list_display = ['number', 'pt_title', 'or_title', 'serie']
    
class EpisodeSerieAdmin(admin.ModelAdmin):
    list_display = ['number', 'pt_title', 'or_title', 'season']

admin.site.register(Serie, SerieAdmin)
admin.site.register(SeasonSerie, SeasonSerieAdmin)
admin.site.register(EpisodeSerie, EpisodeSerieAdmin)
