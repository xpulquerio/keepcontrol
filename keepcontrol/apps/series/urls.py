from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.ListSerie, name='ListSerie'),
    path('<int:id>/', views.ListSeasonSerie, name='ListSeasonSerie'),
    path('<int:serie_id>/<int:season_id>/', views.ListEpisodeSerie, name='ListEpisodeSerie'),
    path('inserir_assistido/<int:episodeserie_id>/', views.InserirAssistido, name='InserirAssistido'),


]