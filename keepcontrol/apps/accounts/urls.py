
from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('entrar/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('sair/', auth_views.LogoutView.as_view(next_page='core:home'), name='logout'),
    path('cadastrar/', views.register, name='register'),
    path('editar/', views.edit, name='edit'),
    path('editar_senha/', views.edit_password, name='edit_password'),
    
    path('cadastrar/', views.register, name='resume'),
    path('series/', views.DashboardSeries, name='DashboardSeries'),
    path('animes/', views.DashboardAnimes, name='DashboardAnimes'),
    path('mangas/', views.DashboardMangas, name='DashboardMangas'),
    path('filmes/', views.DashboardMovies, name='DashboardMovies'),
    path('livros/', views.DashboardBooks, name='DashboardBooks'),
    
    path('favoritos/', views.DashboardFavorites, name='DashboardFavorites'),
]