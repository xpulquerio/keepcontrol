from django.db import models

# Create your models here.
   
class Serie(models.Model):
    title = models.CharField('Título', max_length=255)
    or_title = models.CharField('Título original', null=True, max_length=255, blank=True)
    director = models.CharField('Diretor', null=True, max_length=255, blank=True)
    situation = models.CharField('Situação', null=True, blank=True)
    created_at = models.DateTimeField('Cadastrado em', auto_now_add=True)
    
    def __str__ (self):
        return self.title
    
    def get_absolute_url(self):
        return '/series/'+ str(self.id) #retorna a URL do curso
    
    class Meta:
        verbose_name = 'Série'
        verbose_name_plural = 'Séries'
        ordering = ['created_at']
    