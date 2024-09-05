from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.ListMovie, name='ListMovie'),
    path('inserir_assistido/<int:filme_id>/', views.inserir_assistido, name='inserir_assistido'),
]