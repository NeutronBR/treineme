# Generated by Django 2.0.4 on 2018-05-02 02:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cursos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inscricao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(blank=True, choices=[(0, 'Pendente'), (1, 'Inscrito'), (2, 'Aprovado'), (3, 'Cancelado')], default=1, verbose_name='Situação')),
                ('data_criacao', models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')),
                ('data_atualizacao', models.DateTimeField(auto_now=True, verbose_name='Data de atualização')),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='inscricoes', to='cursos.Curso', verbose_name='Curso')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='inscricoes', to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Inscrição',
                'verbose_name_plural': 'Inscrições',
            },
        ),
        migrations.AlterUniqueTogether(
            name='inscricao',
            unique_together={('curso', 'usuario')},
        ),
    ]
