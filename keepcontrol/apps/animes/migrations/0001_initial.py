# Generated by Django 4.2.2 on 2023-06-27 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Anime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pt_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Título brasileiro')),
                ('or_title', models.CharField(max_length=255, verbose_name='Título original')),
                ('author', models.CharField(blank=True, max_length=255, null=True, verbose_name='Diretor')),
                ('situation', models.CharField(blank=True, null=True, verbose_name='Situação')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Cadastrado em')),
            ],
            options={
                'verbose_name': 'Anime',
                'verbose_name_plural': 'Animes',
                'ordering': ['pt_title'],
            },
        ),
    ]
