from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    list_display = ['or_title', 'pt_title', 'year', 'created_at']
    search_fields = ['or_title', 'pt_title']

admin.site.register(Book, BookAdmin)