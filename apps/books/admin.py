from django.contrib import admin
from .models import Book
from import_export.admin import ImportExportActionModelAdmin

class BookAdmin(ImportExportActionModelAdmin):
    list_display = ['or_title', 'pt_title', 'year', 'created_at']
    search_fields = ['or_title', 'pt_title']
    ordering = ['-created_at']

admin.site.register(Book, BookAdmin)