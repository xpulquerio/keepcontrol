from django.db import models

class Manga(models.Model):
    pt_title = models.CharField('Título brasileiro', max_length=255, blank=True, null=True)
    or_title = models.CharField('Título original', max_length=255)
    author = models.CharField('Autor', null=True, max_length=255, blank=True)
    situation = models.CharField('Situação', null=True, blank=True)
    created_at = models.DateTimeField('Cadastrado em', auto_now_add=True)
    modified_at = models.DateField('Modificado em', auto_now=True)
    
    def __str__ (self):
        if self.pt_title:
            return self.pt_title
        else:
            return self.or_title
    
    def get_absolute_url(self):
        return '/mangas/'+ str(self.id) #retorna a URL do curso
        
    def insert_vols(self, qtd_vol):
            cont = 0
            for i in range(qtd_vol):
                number_of_volume = i+1
                temp = VolumeManga(number=number_of_volume, manga_id=self.id)
                if VolumeManga.objects.filter(number=number_of_volume, manga_id=self.id).exists():
                    print('Volume '+str(number_of_volume)+' já existe')
                    #Se a temporada existe, não fazer nada.
                else:
                    #Se a temporada não existe, inserir no banco.
                    temp.save()
                    print('Volume '+str(temp.number)+' inserida!')
                    cont = cont+1
            return 'Número de volumes adicionadas: '+str(cont)
        
    class Meta:
        verbose_name = 'Manga'
        verbose_name_plural = 'Mangás'
        ordering = ['pt_title']

class VolumeManga(models.Model):
    pt_title = models.CharField('Título brasileiro', max_length=255, blank=True, null=True)
    or_title = models.CharField('Título original', max_length=255, blank=True, null=True)
    number = models.BigIntegerField('Volume')
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE, verbose_name="Mangá")

    def __str__ (self):
        if self.manga.pt_title:
            return f"Volume {self.number} - {self.manga.pt_title}"
        else:
            return f"Volume {self.number} - {self.manga.or_title}"
    
    def get_qtd_volumes(manga_id):
        return VolumeManga.objects.filter(manga_id=manga_id).count() #Número de temporadas da série com este ID
        
    def get_volumes(manga_id):
        return VolumeManga.objects.filter(manga_id=manga_id) #As temporaas da série com este ID
    
    def get_absolute_url(self):
        return '/mangas/'+ str(self.manga_id)+'/'+ str(self.id)
    
    def insert_caps(self, qtd_caps, number_cap):
        cont = 0
        for i in range(qtd_caps):
            x = i+number_cap
            
            temp = ChapterManga(number=x, volume_id=self.id)
            if ChapterManga.objects.filter(number=temp.number, volume_id=temp.volume_id).exists():
                print('Capítulo '+str(x)+' já existe')
                #Se o episódio existir, não fazer nada.
            else:
                #Se o episódio não existir, inserir no banco.
                temp.save()
                print('Capítulo '+str(temp.number)+' inserido!')
                cont = cont+1
            
        return 'Número de capítulos adicionados: '+str(cont)
    
    class Meta:
        verbose_name = 'Volume'
        verbose_name_plural = 'Volume'
            

class ChapterManga(models.Model):
    pt_title = models.CharField('Título brasileiro', max_length=255, blank=True, null=True)
    or_title = models.CharField('Título original', max_length=255, blank=True, null=True)
    number = models.FloatField('Capítulo')
    volume = models.ForeignKey(VolumeManga, on_delete=models.CASCADE, verbose_name="Volume")
    
    def __str__ (self):
        if self.volume.pt_title:
            return f"Capítulo {self.number} - Volume {self.volume.pt_title} - {self.volume.manga}"
        else:
            return f"Capítulo {self.number} - Volume {self.volume.number} - {self.volume.manga}"
    
    def get_qtd_chapters(id):
        return ChapterManga.objects.filter(volume_id=id).count()
    
    def get_chapters(self, volume_id):
        return ChapterManga.objects.filter(volume_id=volume_id)
    
    def insert_eps(self, qtd_caps, volume_id):
        cont = 0
        for i in range(qtd_caps):
            number_of_cap = i+1
            title_of_chapter_for_insert = 'Capítulo '+str(number_of_cap) 
            temp = ChapterManga(number=number_of_cap, volume_id=volume_id)
            if ChapterManga.objects.filter(number=temp.number, volume_id=temp.volume_id).exists():
                print(title_of_chapter_for_insert+' já existe')
                #Se o episódio existir, não fazer nada.
            else:
                #Se o episódio não existir, inserir no banco.
                temp.save()
                print('Capítulo: '+str(temp.number)+' inserido!')
                cont = cont+1
        return 'Número de capítulos adicionados: '+str(cont)
    
    class Meta:
        verbose_name = 'Capítulo'
        verbose_name_plural = 'Capítulos'