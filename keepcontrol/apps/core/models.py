from django.db import models

class Conteudo(models.Model):
    pt_title = models.CharField('Título brasileiro', max_length=255, blank=True, null=True)
    or_title = models.CharField('Título original', max_length=255)
    created_at = models.DateTimeField('Cadastrado em', auto_now_add=True)
    modified_at = models.DateField('Modificado em', auto_now=True)
    
    class Meta:
        abstract = True