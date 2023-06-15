from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.series, name='series'),
    path('<int:id>/', views.details, name='details')
]