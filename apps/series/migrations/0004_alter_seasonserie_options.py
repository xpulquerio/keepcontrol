# Generated by Django 4.2.7 on 2024-07-09 16:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0003_alter_episodeserie_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='seasonserie',
            options={'ordering': ['serie__pt_title', 'number'], 'verbose_name': 'Temporada', 'verbose_name_plural': 'Temporadas'},
        ),
    ]