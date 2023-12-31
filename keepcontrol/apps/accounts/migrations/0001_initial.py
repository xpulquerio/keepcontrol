# Generated by Django 4.2.2 on 2023-06-27 11:56

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('series', '0001_initial'),
        ('animes', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=30, unique=True, validators=[django.core.validators.RegexValidator(re.compile('^[\\w.@=-]+$'), 'O nome de usuário só pode contar, letras, digitos ou @/./+/-/_', 'invalid')], verbose_name='Nome de usuário')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='E-mail')),
                ('name', models.CharField(blank=True, max_length=100, verbose_name='Nome completo')),
                ('is_active', models.BooleanField(blank=True, default=True, verbose_name='Está ativo?')),
                ('is_staff', models.BooleanField(blank=True, default=False, verbose_name='É da equipe')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Data de entrada')),
            ],
            options={
                'verbose_name': 'Usuário',
                'verbose_name_plural': 'Usuários',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserMovie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_watched', models.DateTimeField()),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Filme do Usuário',
                'verbose_name_plural': 'Filmes do Usuário',
            },
        ),
        migrations.CreateModel(
            name='UserEpisodeSerie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_watched', models.DateTimeField()),
                ('episode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='series.episodeserie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Episódio de série do Usuário',
                'verbose_name_plural': 'Episódios de séries do Usuário',
            },
        ),
        migrations.CreateModel(
            name='UserEpisodeAnime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_watched', models.DateTimeField()),
                ('episode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='animes.episodeanime')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Episódio de anime do Usuário',
                'verbose_name_plural': 'Episódios de animes do Usuário',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='episodes_anime',
            field=models.ManyToManyField(blank=True, through='accounts.UserEpisodeAnime', to='animes.episodeanime'),
        ),
        migrations.AddField(
            model_name='user',
            name='episodes_serie',
            field=models.ManyToManyField(blank=True, through='accounts.UserEpisodeSerie', to='series.episodeserie'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='movies',
            field=models.ManyToManyField(blank=True, through='accounts.UserMovie', to='movies.movie'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
