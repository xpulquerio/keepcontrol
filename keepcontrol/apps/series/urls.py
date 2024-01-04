from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.ListSerie, name='ListSerie'),
    path('<int:id>/', views.ListSeasonSerie, name='ListSeasonSerie'),
    path('<int:serie_id>/<int:season_id>/', views.ListEpisodeSerie, name='ListEpisodeSerie'),
    path('inserirepisodeanime/<int:episodeserie_id>/', views.InserirAssistidoEpisodeSerie, name='InserirAssistidoEpisodeSerie'),
    path('inserirseasonserie/<int:season_id>/<int:serie_id>/', views.InserirAssistidoSeasonSerie, name='InserirAssistidoSeasonSerie'),
    path('inserirfavoritaserie/<int:serie_id>/', views.InserirSerieFavorita, name='InserirSerieFavorita'),

]