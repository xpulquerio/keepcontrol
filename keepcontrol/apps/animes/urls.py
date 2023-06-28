from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.ListAnime, name='animes'),
    path('<int:id>/', views.ListSeasonAnime, name='anime_details'),
    path('<int:anime_id>/<int:season_id>/', views.ListEpisodeAnime, name='season_details'),

]