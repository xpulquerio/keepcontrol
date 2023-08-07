from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from apps.accounts.models import UserChapterManga
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q

def ListManga (request):
    
    search_query = request.GET.get('search') #Link com o form-serch no html
    
    if search_query:
        mangas = Manga.objects.filter(
            Q(pt_title__icontains=search_query) |  # Busca por título em português (case-insensitive)
            Q(or_title__icontains=search_query)    # Busca por título em inglês (case-insensitive)
        ).order_by('or_title')
    else:
        mangas = Manga.objects.all().order_by('-created_at')    

    for x in mangas:
        temp_count = VolumeManga.get_qtd_volumes(x.id)
        x.qtd_vols = temp_count
    
    movies_paginator = Paginator(mangas, 20) #Filtra apenas 20 de todos os animes
    
    page_num = request.GET.get('page')
   
    page = movies_paginator.get_page(page_num)
    
    template_name = 'ListManga.html'
    context = {
        'page': page,
        'qtd_mangas' : mangas.count,
        'qtd_pages': movies_paginator.num_pages,
        'search_query': search_query  # Passar o valor de busca para o template
    }

    return render(request, template_name, context)

def ListVolumeManga (request, id):
    context = {}

    manga = get_object_or_404(Manga, id=id)
    manga.qtd_vols = VolumeManga.get_qtd_volumes(id) #Incluindo quantidade de temporadas como atributo de anime
    manga.qtd_total_caps = 0

    volumes = VolumeManga.objects.filter(manga_id=id).order_by('number')
        
    for volume in volumes:
        volume.qtd_lido = 0
        volume.qtd_caps = ChapterManga.get_qtd_chapters(volume.id)
        manga.qtd_total_caps += volume.qtd_caps
        if request.user.is_authenticated:
            chapters = ChapterManga.objects.filter(volume=volume.id)
            for cap in chapters:
                if cap in request.user.chapters_manga.all():
                    volume.qtd_lido += 1
    
    template_name = 'ListVolumeManga.html'
    context = {
        'volumes': volumes,
        'manga': manga
    }  
    return render(request, template_name, context)

def ListChapterManga (request, manga_id, volume_id):
    context = {}
    
    volume = VolumeManga.objects.filter(id=volume_id)
    manga = Manga.objects.filter(id=manga_id)
    caps = ChapterManga.objects.filter(volume_id=volume_id).order_by('number')
    
    usuario = request.user #Pegando o usuário logado
    
    for cap in caps:
        user_chapter = cap.userchaptermanga_set.filter(user=usuario.id).first()
        if user_chapter and user_chapter.date_watched:
            cap.date_watched = user_chapter.date_watched
    
    template_name = 'ListChapterManga.html'
    context = {
        'caps': caps,
        'volume': volume.first(),
        'manga': manga.first()
    }
    
    return render(request, template_name, context)

@login_required
def InserirLidoChapterManga(request, chapter_id):
    chapter_manga = ChapterManga.objects.filter(id=chapter_id).first()
    volume_id = chapter_manga.volume.id
    manga_id = chapter_manga.volume.manga_id
    
    usuario = request.user
    chaptermanga_user = UserChapterManga.objects.filter(user=usuario.id, chapter=chapter_id)
    
    if chaptermanga_user:
        print (str(chaptermanga_user)+" já foi lido pelo usuário")
        return redirect('mangas:ListChapterManga', manga_id=manga_id, volume_id=volume_id)
    else:
        x = UserChapterManga(chapter=chapter_manga, user=usuario, date_watched=timezone.now()) #Depois alterar o banco para inserir a data automaticamente
        x.save()
        print (str(chapter_manga)+" inserido!")
        return redirect('mangas:ListChapterManga', manga_id=manga_id, volume_id=volume_id)

@login_required
def InserirLidoVolumeManga(request, volume_id, manga_id):
    chapters_manga = ChapterManga.objects.filter(volume=volume_id)
    
    for cap in chapters_manga:
        x = cap.id
        print(x)
        InserirLidoChapterManga(request=request,chapter_id=x)
        
    return redirect('mangas:ListVolumeManga', id=manga_id)
        
