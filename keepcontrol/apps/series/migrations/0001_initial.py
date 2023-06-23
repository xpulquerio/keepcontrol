# Generated by Django 4.2.2 on 2023-06-22 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Serie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Título')),
                ('or_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Título original')),
                ('director', models.CharField(blank=True, max_length=255, null=True, verbose_name='Diretor')),
                ('situation', models.CharField(blank=True, null=True, verbose_name='Situação')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Cadastrado em')),
            ],
            options={
                'verbose_name': 'Série',
                'verbose_name_plural': 'Séries',
                'ordering': ['created_at'],
            },
        ),
    ]
