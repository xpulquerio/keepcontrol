from django.contrib import admin
from .models import Movie

class MovieAdmin(admin.ModelAdmin):
    list_display = ['or_title', 'pt_title', 'year', 'created_at']

admin.site.register(Movie, MovieAdmin)
