# Generated by Django 2.0.6 on 2018-06-24 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0017_auto_20180623_2005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inscricao',
            name='nota_curso',
            field=models.IntegerField(blank=True, choices=[(1, 'Muito insatisfeito'), (2, 'Insatisfeito'), (3, 'Regular'), (4, 'Satisfeito'), (5, 'Muito satisfeito')], default=None, null=True, verbose_name='Nota do curso'),
        ),
    ]
