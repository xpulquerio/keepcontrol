from django.db import models


class Serie(models.Model):
    pt_title = models.CharField('Título brasileiro', max_length=255, blank=True, null=True)
    or_title = models.CharField('Título original', max_length=255)
    director = models.CharField('Diretor', null=True, max_length=255, blank=True)
    situation = models.CharField('Situação', null=True, blank=True)
    created_at = models.DateTimeField('Cadastrado em', auto_now_add=True)
    modified_at = models.DateField('Modificado em', auto_now=True)
    
    def __str__ (self):
        if self.pt_title:
            return self.pt_title
        else:
            return self.or_title
    
    def get_absolute_url(self):
        return '/series/'+ str(self.id) #retorna a URL do curso

    def insert_temps(self, qtd_temps):
            cont = 0
            for i in range(qtd_temps):
                number_of_season = i+1
            
                temp = SeasonSerie(number=number_of_season, serie_id=self.id)
                if SeasonSerie.objects.filter(number=temp.number, serie_id=temp.serie_id).exists():
                    print('Temporada '+str(number_of_season)+' já existe')
                    #Se a temporada existe, não fazer nada.
                else:
                    #Se a temporada não existe, inserir no banco.
                    temp.save()
                    print('Temporada '+str(temp.number)+' inserida!')
                    cont = cont+1
            return 'Número de temporadas adicionadas: '+str(cont)
        
    class Meta: 
        verbose_name = 'Série'
        verbose_name_plural = 'Séries'
        ordering = ['pt_title']

class SeasonSerie(models.Model):
    pt_title = models.CharField('Título brasileiro', max_length=255, blank=True, null=True)
    or_title = models.CharField('Título original', max_length=255, blank=True, null=True)
    number = models.BigIntegerField('Temporada')
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE, verbose_name="Série")

    def __str__ (self):
        if self.serie.pt_title:
            return f"{self.serie.pt_title} - Temporada {self.number}"
        else:
            return f"{self.serie.or_title} - Season {self.number}"
    
    def get_qtd_seasons(serie_id):
        return SeasonSerie.objects.filter(serie_id=serie_id).count() #Número de temporadas da série com este ID
        
    def get_seasons(serie_id):
        return SeasonSerie.objects.filter(serie_id=serie_id) #As temporaas da série com este ID
    
    def get_absolute_url(self):
        return '/series/'+ str(self.serie_id)+'/'+ str(self.id)
    
    def insert_eps(self, qtd_eps):
        cont = 0
        for i in range(qtd_eps):
            number_of_ep = i+1
            title_of_episode_for_insert = 'Episódio '+str(number_of_ep) 
            id_of_season = self.id
            temp = EpisodeSerie(number=number_of_ep, season_id=id_of_season)
            if EpisodeSerie.objects.filter(number=temp.number, season_id=temp.season_id).exists():
                print(title_of_episode_for_insert+' já existe')
                #Se o episódio existir, não fazer nada.
            else:
                #Se o episódio não existir, inserir no banco.
                temp.save()
                print('EP: '+str(temp.number)+' inserido!')
                cont = cont+1
        return 'Número de episódios adicionados: '+str(cont)
    
    class Meta:
        verbose_name = 'Temporada'
        verbose_name_plural = 'Temporadas'
        unique_together = ['number', 'serie']
        ordering = ['serie__pt_title', 'number']
            
class EpisodeSerie(models.Model):
    pt_title = models.CharField('Título brasileiro', max_length=255, blank=True, null=True)
    or_title = models.CharField('Título original', max_length=255, blank=True, null=True)
    number = models.BigIntegerField('Episódio')
    season = models.ForeignKey(SeasonSerie, on_delete=models.CASCADE, verbose_name="Temporada")
    
    def __str__ (self):
        if self.season.pt_title:
            return f"Episódio {self.number} - {self.season.pt_title} - {self.season.serie}"
        else:
            return f"Episódio {self.number} - Temporada {self.season.number} - {self.season.serie}"
    
    def get_qtd_episodes(season_id):
        return EpisodeSerie.objects.filter(season_id=season_id).count()
    
    def get_episodes(self, season_id):
        return EpisodeSerie.objects.filter(season_id=season_id)
        
    class Meta:
        verbose_name = 'Episódio'
        verbose_name_plural = 'Episódios'
        unique_together = ['number', 'season']