from django.db import models


# Create your models here.
   
class Serie(models.Model):
    pt_title = models.CharField('Título brasileiro', max_length=255, blank=True, null=True)
    or_title = models.CharField('Título original', max_length=255)
    director = models.CharField('Diretor', null=True, max_length=255, blank=True)
    situation = models.CharField('Situação', null=True, blank=True)
    created_at = models.DateTimeField('Cadastrado em', auto_now_add=True)
    
    def __str__ (self):
        return self.pt_title
    
    def get_absolute_url(self):
        return '/series/'+ str(self.id) #retorna a URL do curso
        
    class Meta:
        verbose_name = 'Série'
        verbose_name_plural = 'Séries'
        ordering = ['pt_title']
    