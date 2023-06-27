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
        
    def insert_temps(self, qtd_temps):
            from apps.core.models import Season #Importando dentro da função para evitar importação circular
            cont = 0
            for i in range(qtd_temps):
                nummber_of_season = i+1
                title_of_season_for_insert = 'Temporada '+str(nummber_of_season) 
                id_of_serie = self.id
                temp = Season(title=title_of_season_for_insert, serie_id=id_of_serie)
                if Season.objects.filter(title=temp.title, serie_id=temp.serie_id).exists():
                    print(title_of_season_for_insert+' já existe')
                    #Se a temporada existe, não fazer nada.
                else:
                    #Se a temporada não existe, inserir no banco.
                    temp.save()
                    print(temp.title+' inserida!')
                    cont = cont+1
            return 'Número de temporadas adicionadas: '+str(cont)
        
    class Meta:
        verbose_name = 'Série'
        verbose_name_plural = 'Séries'
        ordering = ['title']
    