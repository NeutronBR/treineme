# Generated by Django 2.0.6 on 2018-06-23 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0015_auto_20180623_1848'),
    ]

    operations = [
        migrations.AddField(
            model_name='inscricao',
            name='comentario',
            field=models.TextField(null=True, verbose_name='Comentário do curso'),
        ),
    ]
