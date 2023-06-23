from django.contrib import admin
from .models import Season, Episode, UserEpisode, UserMovie

class SeasonAdmin(admin.ModelAdmin):
    fields = ['title', 'serie']
    
class EpisodeAdmin(admin.ModelAdmin):
    fields = ['title', 'season']

class UserEpisodeAdmin(admin.ModelAdmin):
    list_display = ['user', 'episode']
    
class UserMovieAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie']   

admin.site.register(Season, SeasonAdmin)
admin.site.register(Episode, EpisodeAdmin)
admin.site.register(UserEpisode, UserEpisodeAdmin)
admin.site.register(UserMovie, UserMovieAdmin)
# Register your models here.
