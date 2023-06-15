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
    or_title = models.CharField('Título original', null=True, max_length=255, blank=True)
    director = models.CharField('Diretor', null=True, max_length=255, blank=True)
    collection = models.CharField('Coleção', null=True, max_length=255, blank=True)
    year = models.IntegerField('Ano', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = MovieManager()

    def __str__ (self):
        return self.title
    
    class Meta:
        verbose_name = 'Filme'
        verbose_name_plural = 'Filmes'
        ordering = ['-created_at']
    