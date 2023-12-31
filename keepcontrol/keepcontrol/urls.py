"""
URL configuration for keepcontrol project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from apps.core import views

urlpatterns = [ 
    path('', include(('apps.core.urls', 'core'), namespace='core')),
    path('animes/', include(('apps.animes.urls', 'animes'), namespace='animes')),
    path('filmes/', include(('apps.movies.urls', 'movies'), namespace='movies')),    
    path('series/', include(('apps.series.urls', 'series'), namespace='series')),
    path('livros/', include(('apps.books.urls', 'books'), namespace='books')),    
    path('mangas/', include(('apps.mangas.urls', 'mangas'), namespace='mangas')), 
    path('conta/', include(('apps.accounts.urls','accounts'), namespace='accounts')) ,
    path('admin/', admin.site.urls)
]
