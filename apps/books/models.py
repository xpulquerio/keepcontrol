from django.db import models

class BookManager(models.Manager): #Custom Manager para fazer pesquisas... Movies.objects.search('nome')

    def search(self, query):
        return self.get_queryset().filter(
            models.Q(pt_title__icontains=query) | 
            models.Q(or_title__icontains=query)
            )
   
class Book(models.Model):
    pt_title = models.CharField('Título brasileiro', max_length=255, blank=True, null=True)
    or_title = models.CharField('Título original', max_length=255)
    resume = models.TextField('Resumo', max_length=2500, blank=True, null=True)
    author = models.CharField('Autor', null=True, max_length=255, blank=True)
    collection = models.CharField('Coleção', null=True, max_length=255, blank=True)
    year = models.IntegerField('Ano', null=True, blank=True)
    created_at = models.DateTimeField('Cadastrado em', auto_now_add=True)

    objects = BookManager()

    def __str__ (self):
        if self.pt_title:
            return self.pt_title
        else:
            return self.or_title
    
    class Meta:
        verbose_name = 'Livro'
        verbose_name_plural = 'Livros'
        ordering = ['pt_title']