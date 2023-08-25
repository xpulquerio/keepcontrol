from django.db import models
from apps.core.models import Conteudo

class MovieManager(models.Manager): #Custom Manager para fazer pesquisas... Movies.objects.search('nome')

    def search(self, query):
        return self.get_queryset().filter(
            models.Q(pt_title__icontains=query) | 
            models.Q(or_title__icontains=query)
            ).order_by('pt_title')
   
class Movie(Conteudo):
    director = models.CharField('Diretor', null=True, max_length=255, blank=True)
    collection = models.CharField('Coleção', null=True, max_length=255, blank=True)
    year = models.IntegerField('Ano', null=True, blank=True)

    objects = MovieManager()

    def __str__ (self):
        if self.pt_title:
            return self.pt_title
        else:
            return self.or_title
    
    class Meta:
        verbose_name = 'Filme'
        verbose_name_plural = 'Filmes'
        ordering = ['pt_title']