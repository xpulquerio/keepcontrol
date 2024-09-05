from django.db import models

class MovieManager(models.Manager): #Custom Manager para fazer pesquisas... Movies.objects.search('nome')

    def search(self, query):
        return self.get_queryset().filter(
            models.Q(pt_title__icontains=query) | 
            models.Q(or_title__icontains=query)
            ).order_by('pt_title')
   
class Movie(models.Model):
    pt_title = models.CharField('Título brasileiro', max_length=255, blank=True, null=True)
    or_title = models.CharField('Título original', max_length=255)
    director = models.CharField('Diretor', null=True, max_length=255, blank=True)
    collection = models.CharField('Coleção', null=True, max_length=255, blank=True)
    year = models.IntegerField('Ano', null=True, blank=True)
    created_at = models.DateTimeField('Cadastrado em', auto_now_add=True)

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