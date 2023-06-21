from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.series, name='series'),
    path('<int:id>/', views.serie_details, name='serie_details'),
    path('<int:serie_id>/<int:season_id>/', views.season_details, name='season_details')

]