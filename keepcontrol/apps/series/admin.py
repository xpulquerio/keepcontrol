from django.contrib import admin
from .models import Serie

class SerieAdmin(admin.ModelAdmin):
    search_fields = ['pt_title', 'or_title']
    list_display = ['pt_title', 'director', 'situation', 'created_at']

admin.site.register(Serie, SerieAdmin)

# Register your models here.
