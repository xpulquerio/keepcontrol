from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.ListBook, name='ListBook'),
    path('inserirlido/<int:book_id>/', views.InserirLido, name='InserirLido'),
]