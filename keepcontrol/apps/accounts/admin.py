from django.contrib import admin
from django.contrib.auth import get_user_model #Para usar o model do nosso usuário
from .models import UserEpisodeAnime, UserEpisodeSerie, UserMovie, UserBook, UserChapterManga, FavoriteAnime, FavoriteBook, FavoriteManga, FavoriteMovie, FavoriteSerie

User = get_user_model()

class UserAdmin(admin.ModelAdmin):
    list_display = ['username','name','email']
    search_fields = ['name']
    filter_horizontal = ('episodes_anime', 'episodes_serie', 'movies')

admin.site.register(User, UserAdmin)

# ------------ ADMIN DO CONTEÚDO DO USUÁRIO ---------- #

class UserEpisodeSerieAdmin(admin.ModelAdmin):
    list_display = ['episode','user', 'date_watched']
    
class UserEpisodeAnimeAdmin(admin.ModelAdmin):
    list_display = ['episode', 'user','date_watched']
    
class UserMovieAdmin(admin.ModelAdmin):
    list_display = ['movie', 'user', 'date_watched']
    ordering = ['movie__or_title']
    
class UserChapterMangaAdmin(admin.ModelAdmin):
    list_display = ['chapter', 'user', 'date_watched']
    
class UserBookAdmin(admin.ModelAdmin):
    list_display = ['book', 'user', 'date_watched']

admin.site.register(UserEpisodeSerie, UserEpisodeSerieAdmin)
admin.site.register(UserEpisodeAnime, UserEpisodeAnimeAdmin)
admin.site.register(UserMovie, UserMovieAdmin)
admin.site.register(UserChapterManga, UserChapterMangaAdmin)
admin.site.register(UserBook, UserBookAdmin)

# --------------- ADMIN DOS FAVORITOS -------------- #

class FavoriteSerieAdmin(admin.ModelAdmin):
    list_display = ['serie','user', 'created_at']
    
class FavoriteAnimeAdmin(admin.ModelAdmin):
    list_display = ['anime', 'user','created_at']
    
class FavoriteMovieAdmin(admin.ModelAdmin):
    list_display = ['movie', 'user', 'created_at']
    
class FavoriteMangaAdmin(admin.ModelAdmin):
    list_display = ['manga', 'user', 'created_at']
    
class FavoriteBookAdmin(admin.ModelAdmin):
    list_display = ['book', 'user', 'created_at']

admin.site.register(FavoriteSerie, FavoriteSerieAdmin)
admin.site.register(FavoriteAnime, FavoriteAnimeAdmin)
admin.site.register(FavoriteMovie, FavoriteMovieAdmin)
admin.site.register(FavoriteManga, FavoriteMangaAdmin)
admin.site.register(FavoriteBook, FavoriteBookAdmin)
# Register your models here.
