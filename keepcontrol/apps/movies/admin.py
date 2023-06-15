from django.contrib import admin
from .models import Movie

class MovieAdmin(admin.ModelAdmin):
    search_fields = ['title', 'or_title']
    list_display = ['title', 'director', 'year', 'created_at']

admin.site.register(Movie, MovieAdmin)