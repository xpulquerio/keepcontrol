from django.shortcuts import render, redirect
from .models import Book
from apps.books.models import Book
from apps.accounts.models import UserBook
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q

# Create your models here.
def ListBook(request):
    
    search_query = request.GET.get('search')
    
    if search_query:
        books = Book.objects.filter(
            Q(pt_title__icontains=search_query) |  # Busca por título em português (case-insensitive)
            Q(or_title__icontains=search_query)    # Busca por título em inglês (case-insensitive)
        ).order_by('pt_title')
    else:
        books = Book.objects.all().order_by('collection', '-year')
    
    usuario = request.user
    
    for book in books:
        user_book = book.userbook_set.filter(user=usuario.id).first()
        if user_book and user_book.date_watched:
            book.date_watched = user_book.date_watched
    
    movies_paginator = Paginator(books, 20)
    
    page_num = request.GET.get('page')
   
    page = movies_paginator.get_page(page_num)
    
    template_name = 'ListBook.html'
    context = {
        'page': page,
        'qtd_books': movies_paginator.count,
        'qtd_pages': movies_paginator.num_pages,
        'search_query': search_query  # Passar o valor de busca para o template
    }

    return render(request, template_name, context)

@login_required
def InserirLido(request, book_id):
    usuario = request.user
    book_user = UserBook.objects.filter(user=usuario.id, book=book_id)
    if book_user:
        print (str(book_user)+" já foi lido pelo usuário")
        return redirect('books:ListBook')
    else:
        b = Book.objects.filter(id=book_id).first()
        x = UserBook(book=b, user=usuario, date_watched=timezone.now()) #Depois alterar o banco para inserir a data automaticamente
        x.save()
        print (str(x)+" inserido!")
        return redirect('books:ListBook')