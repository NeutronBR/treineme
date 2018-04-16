# Generated by Django 2.0.3 on 2018-04-14 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('atalho', models.SlugField(unique=True)),
                ('instrutor', models.CharField(max_length=100, verbose_name='Nome do instrutor')),
                ('descricao', models.TextField(verbose_name='Descrição curta do curso')),
                ('sobre', models.TextField(blank=True, verbose_name='Descrição completa do curso')),
                ('keywords', models.TextField(blank=True, verbose_name='Palavras-chave')),
                ('data_criacao', models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')),
                ('data_atualizacao', models.DateTimeField(auto_now=True, verbose_name='Data de atualização')),
                ('categoria', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cursos.Categoria')),
            ],
            options={
                'verbose_name': 'Curso',
                'verbose_name_plural': 'Cursos',
                'ordering': ['nome'],
            },
        ),
    ]
