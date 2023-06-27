from django.contrib import admin
from .models import Season, Episode, UserEpisode, UserMovie

class SeasonAdmin(admin.ModelAdmin):
    fields = ['pt_title', 'serie']
    search_fields = ['pt_title', 'or_title', 'number', 'serie']
    
class EpisodeAdmin(admin.ModelAdmin):
    fields = ['number', 'season', 'pt_title']
    search_fields = ['pt_title', 'or_title', 'number', 'season']

class UserEpisodeAdmin(admin.ModelAdmin):
    list_display = ['user', 'episode']
    search_fields = ['user', 'episode']

    
class UserMovieAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie']
    search_fields = ['user', 'episode']


admin.site.register(Season, SeasonAdmin)
admin.site.register(Episode, EpisodeAdmin)
admin.site.register(UserEpisode, UserEpisodeAdmin)
admin.site.register(UserMovie, UserMovieAdmin)
# Register your models here.
