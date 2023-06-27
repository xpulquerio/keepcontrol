from django.db import models

# Create your models here.
   
class Anime(models.Model):
    pt_title = models.CharField('Título brasileiro', max_length=255, blank=True, null=True)
    or_title = models.CharField('Título original', max_length=255)
    author = models.CharField('Diretor', null=True, max_length=255, blank=True)
    situation = models.CharField('Situação', null=True, blank=True)
    created_at = models.DateTimeField('Cadastrado em', auto_now_add=True)
    
    def __str__ (self):
        return self.pt_title
    
    def get_absolute_url(self):
        return '/animes/'+ str(self.id) #retorna a URL do curso
        
    def insert_temps(self, qtd_temps):
            from apps.core.models import Season #Importando dentro da função para evitar importação circular
            cont = 0
            for i in range(qtd_temps):
                nummber_of_season = i+1
                title_of_season_for_insert = 'Temporada '+str(nummber_of_season) 
                id_of_anime = self.id
                temp = Season(pt_title=title_of_season_for_insert, anime_id=id_of_anime)
                if Season.objects.filter(pt_title=temp.pt_title, anime_id=temp.anime_id).exists():
                    print(title_of_season_for_insert+' já existe')
                    #Se a temporada existe, não fazer nada.
                else:
                    #Se a temporada não existe, inserir no banco.
                    temp.save()
                    print(temp.pt_title+' inserida!')
                    cont = cont+1
            return 'Número de temporadas adicionadas: '+str(cont)
        
    class Meta:
        verbose_name = 'Anime'
        verbose_name_plural = 'Animes'
        ordering = ['pt_title']
    