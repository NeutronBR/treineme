# Generated by Django 2.0.6 on 2018-06-23 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0013_remove_curso_keywords'),
    ]

    operations = [
        migrations.AddField(
            model_name='inscricao',
            name='nota',
            field=models.FloatField(default=0, verbose_name='Nota'),
        ),
        migrations.AddField(
            model_name='inscricao',
            name='qtd_videos',
            field=models.FloatField(default=0, verbose_name='Vídeos Assistidos'),
        ),
    ]
