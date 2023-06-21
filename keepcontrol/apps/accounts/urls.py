
from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('entrar/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('sair/', auth_views.LogoutView.as_view(next_page='core:home'), name='logout'),
]