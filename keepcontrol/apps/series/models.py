from django.db import models

# Create your models here.
   
class Serie(models.Model):
    title = models.CharField('Título', max_length=255)
    title_en = models.CharField('Título em Inglês', null=True, max_length=255, blank=True)
    autor = models.CharField('Autor', null=True, max_length=255, blank=True)
    situation = models.CharField('Situação', null=True, blank=True)
    
    def __str__ (self):
        return self.title
    
    def get_absolute_url(self):
        return '/series/'+ str(self.id) #retorna a URL do curso
    
    class Meta:
        verbose_name = 'Série'
        verbose_name_plural = 'Séries'
    