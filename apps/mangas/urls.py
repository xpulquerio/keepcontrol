from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.ListManga, name='ListManga'),
    path('<int:id>/', views.ListVolumeManga, name='ListVolumeManga'),
    path('<int:manga_id>/<int:volume_id>/', views.ListChapterManga, name='ListChapterManga'),
    path('inserirchaptermanga/<int:chapter_id>/', views.InserirLidoChapterManga, name='InserirLidoChapterManga'),
    path('inserirvolumemanga/<int:volume_id>/<int:manga_id>/', views.InserirLidoVolumeManga, name='InserirLidoVolumeManga'),
]