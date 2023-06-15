from django.contrib import admin
from .models import Serie

class SerieAdmin(admin.ModelAdmin):
    search_fields = ['title', 'or_title']
    list_display = ['title', 'director', 'situation', 'created_at']

admin.site.register(Serie, SerieAdmin)

# Register your models here.
