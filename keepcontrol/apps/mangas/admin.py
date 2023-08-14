from django.contrib import admin
from .models import Manga, VolumeManga, ChapterManga

class MangaAdmin(admin.ModelAdmin):
    list_display = ['or_title','pt_title', 'author', 'situation', 'created_at']
    ordering = ['-created_at']

class VolumeMangaAdmin(admin.ModelAdmin):
    list_display = ['display_number', 'pt_title', 'or_title', 'manga']
    
    def display_number(self, obj): #Substitui a exibição do campo number pelo método abaixo e utiliza esse método no list_display para exibir
        return f"Volume {obj.number}"
    display_number.short_description = "Volume" #Cria a descrição curta para exibir no cabeçalho da tabela
    
class ChapterMangaAdmin(admin.ModelAdmin):
    list_display = ['display_number', 'pt_title', 'or_title', 'volume']
    search_fields = ['number','or_title', 'volume__or_title', 'volume__manga__or_title']
    def display_number(self, obj): #Substitui a exibição do campo number pelo método abaixo e utiliza esse método no list_display para exibir
        return f"Capítulo {obj.number}"
    display_number.short_description = "Capítulo" #Cria a descrição curta para exibir no cabeçalho da tabela
        
admin.site.register(Manga, MangaAdmin)
admin.site.register(VolumeManga, VolumeMangaAdmin)
admin.site.register(ChapterManga, ChapterMangaAdmin)