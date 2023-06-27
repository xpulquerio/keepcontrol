from django.db import models

class Anime(models.Model):
    pt_title = models.CharField('Título brasileiro', max_length=255, blank=True, null=True)
    or_title = models.CharField('Título original', max_length=255)
    author = models.CharField('Author', null=True, max_length=255, blank=True)
    situation = models.CharField('Situação', null=True, blank=True)
    created_at = models.DateTimeField('Cadastrado em', auto_now_add=True)
    
    def __str__ (self):
        if self.pt_title:
            return self.pt_title
        else:
            return self.or_title
    
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

class SeasonAnime(models.Model):
    pt_title = models.CharField('Título brasileiro', max_length=255, blank=True, null=True)
    or_title = models.CharField('Título original', max_length=255, blank=True, null=True)
    number = models.BigIntegerField('Temporada')
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, verbose_name="Anime")

    def __str__ (self):
        if self.anime.pt_title:
            return f"Temporada {self.number} - {self.anime.pt_title}"
        else:
            return f"Temporada {self.number} - {self.anime.or_title}"
    
    def get_qtd_seasons(anime_id):
        return SeasonAnime.objects.filter(anime_id=anime_id).count() #Número de temporadas da série com este ID
        
    def get_seasons(anime_id):
        return SeasonAnime.objects.filter(anime_id=anime_id) #As temporaas da série com este ID
    
    def get_absolute_url(self):
        return '/animes/'+ str(self.anime_id)+'/'+ str(self.id)
    
    def insert_eps(self, qtd_eps):
        cont = 0
        for i in range(qtd_eps):
            number_of_ep = i+1
            title_of_episode_for_insert = 'Episódio '+str(number_of_ep) 
            id_of_season = self.id
            temp = EpisodeAnime(number=number_of_ep, season_id=id_of_season)
            if EpisodeAnime.objects.filter(number=temp.number, season_id=temp.season_id).exists():
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
            

class EpisodeAnime(models.Model):
    pt_title = models.CharField('Título brasileiro', max_length=255, blank=True, null=True)
    or_title = models.CharField('Título original', max_length=255, blank=True, null=True)
    number = models.BigIntegerField('Episódio')
    season = models.ForeignKey(SeasonAnime, on_delete=models.CASCADE, verbose_name="Temporada")
    
    def __str__ (self):
        if self.season.pt_title or self.season.or_title:
            return f"Episódio {self.number}: {self.season.pt_title}" or f"Episódio {self.number}: {self.season.or_title}"
        else:
            return f"Episódio {self.number}"
    
    def get_qtd_episodes(id):
        return EpisodeAnime.objects.filter(season_id=id).count()
    
    def get_episodes(self, id_da_season):
        return EpisodeAnime.objects.filter(season_id=id_da_season)
    
    def insert_eps(self, qtd_eps, season_id):
        cont = 0
        for i in range(qtd_eps):
            number_of_ep = i+1
            title_of_episode_for_insert = 'Episódio '+str(number_of_ep) 
            temp = EpisodeAnime(number=number_of_ep, season_id=season_id)
            if EpisodeAnime.objects.filter(number=temp.number, season_id=temp.season_id).exists():
                print(title_of_episode_for_insert+' já existe')
                #Se o episódio existir, não fazer nada.
            else:
                #Se o episódio não existir, inserir no banco.
                temp.save()
                print('EP: '+str(temp.number)+' inserido!')
                cont = cont+1
        return 'Número de episódios adicionados: '+str(cont)
    
    class Meta:
        verbose_name = 'Episódio'
        verbose_name_plural = 'Episódios'