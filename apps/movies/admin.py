from django.contrib import admin
from .models import Movie
from import_export.admin import ImportExportActionModelAdmin

class MovieAdmin(ImportExportActionModelAdmin):
    list_display = ['or_title', 'pt_title', 'year', 'created_at']
    search_fields = ['or_title', 'pt_title']
    ordering = ['-created_at']

admin.site.register(Movie, MovieAdmin)
