from django.db import models

# Create your models here.
class MovieManager(models.Manager): #Custom Manager para fazer pesquisas... Movies.objects.search('nome')

    def search(self, query):
        return self.get_queryset().filter(
            models.Q(title__icontains=query) | 
            models.Q(title_en__icontains=query)
            )
   
class Movie(models.Model):
    title = models.CharField('Título', max_length=255)
    title_en = models.CharField('Título em inglês', null=True, max_length=255, blank=True)
    autor = models.CharField('Autor', null=True, max_length=255, blank=True)
    collection = models.CharField('Coleção', null=True, max_length=255, blank=True)
    year = models.IntegerField('Ano', null=True, blank=True)

    objects = MovieManager()

    def __str__ (self):
        return self.title
    
    class Meta:
        verbose_name = 'Filme'
        verbose_name_plural = 'Filmes'
        ordering = ['collection', 'title']
    