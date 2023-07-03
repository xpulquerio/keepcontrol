from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.ListAnime, name='ListAnime'),
    path('<int:id>/', views.ListSeasonAnime, name='ListSeasonAnime'),
    path('<int:anime_id>/<int:season_id>/', views.ListEpisodeAnime, name='ListEpisodeAnime'),
    path('inserir_assistido/<int:episodeanime_id>/', views.InserirAssistido, name='InserirAssistido'),


]