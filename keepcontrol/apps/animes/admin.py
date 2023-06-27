from django.contrib import admin
from .models import Anime

class AnimeAdmin(admin.ModelAdmin):
    search_fields = ['pt_title', 'or_title']
    list_display = ['pt_title', 'author', 'situation', 'created_at']

admin.site.register(Anime, AnimeAdmin)