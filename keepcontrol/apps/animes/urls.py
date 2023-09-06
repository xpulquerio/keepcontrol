from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.ListAnime, name='ListAnime'),
    path('<int:id>/', views.ListSeasonAnime, name='ListSeasonAnime'),
    path('<int:anime_id>/<int:season_id>/', views.ListEpisodeAnime, name='ListEpisodeAnime'),
    path('inserirepisodeanime/<int:episode_id>/', views.InserirAssistidoEpisodeAnime, name='InserirAssistidoEpisodeAnime'),
    path('inserirseasonanime/<int:season_id>/<int:anime_id>/', views.InserirAssistidoSeasonAnime, name='InserirAssistidoSeasonAnime'),
    path('inserirfavoritoanime/<int:anime_id>/', views.InserirAnimeFavorito, name='InserirAnimeFavorito'),
    
]