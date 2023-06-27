from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.animes, name='animes'),
    path('<int:id>/', views.anime_details, name='anime_details'),
    path('<int:anime_id>/<int:season_id>/', views.season_details, name='season_details'),

]