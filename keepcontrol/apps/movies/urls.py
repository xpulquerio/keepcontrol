from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.movies, name='movies'),
]