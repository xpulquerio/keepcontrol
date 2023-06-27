from django.contrib import admin
from django.contrib.auth import get_user_model #Para usar o model do nosso usuário

User = get_user_model()

class UserAdmin(admin.ModelAdmin):
    list_display = ['username','name','email']
    search_fields = ['name']
    filter_horizontal = ('episodes_anime', 'episodes_serie', 'movies')

admin.site.register(User, UserAdmin)

# Register your models here.
