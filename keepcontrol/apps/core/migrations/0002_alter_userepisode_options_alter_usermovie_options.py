# Generated by Django 4.2.2 on 2023-06-23 00:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userepisode',
            options={'verbose_name': 'Episódio do Usuário', 'verbose_name_plural': 'Episódios do Usuário'},
        ),
        migrations.AlterModelOptions(
            name='usermovie',
            options={'verbose_name': 'Filme do Usuário', 'verbose_name_plural': 'Filmes do Usuário'},
        ),
    ]
