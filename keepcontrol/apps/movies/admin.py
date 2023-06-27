from django.contrib import admin
from .models import Movie

class MovieAdmin(admin.ModelAdmin):
    search_fields = ['pt_title', 'or_title']
    list_display = ['pt_title', 'year', 'created_at']

admin.site.register(Movie, MovieAdmin)