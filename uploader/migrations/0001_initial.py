# Generated by Django 2.2 on 2019-04-29 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Culturatemp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=250)),
                ('nome', models.CharField(max_length=250)),
                ('prot', models.CharField(blank=True, max_length=250, null=True)),
                ('medico', models.CharField(blank=True, max_length=250, null=True)),
                ('data', models.DateTimeField(blank=True, null=True)),
                ('unid', models.CharField(blank=True, max_length=250, null=True)),
                ('coleta', models.DateTimeField(blank=True, null=True)),
                ('material', models.CharField(blank=True, max_length=250, null=True)),
                ('mat_especifico', models.CharField(blank=True, max_length=250, null=True)),
                ('resultado', models.CharField(blank=True, max_length=250, null=True)),
                ('tipo', models.CharField(blank=True, max_length=250, null=True)),
                ('testes', models.CharField(blank=True, max_length=250, null=True)),
                ('falha', models.CharField(blank=True, max_length=250, null=True)),
                ('ami', models.CharField(blank=True, max_length=250, null=True)),
                ('amp', models.CharField(blank=True, max_length=250, null=True)),
                ('asb', models.CharField(blank=True, max_length=250, null=True)),
                ('atm', models.CharField(blank=True, max_length=250, null=True)),
                ('caz', models.CharField(blank=True, max_length=250, null=True)),
                ('cip', models.CharField(blank=True, max_length=250, null=True)),
                ('cli', models.CharField(blank=True, max_length=250, null=True)),
                ('cpm', models.CharField(blank=True, max_length=250, null=True)),
                ('cro', models.CharField(blank=True, max_length=250, null=True)),
                ('ctn', models.CharField(blank=True, max_length=250, null=True)),
                ('eri', models.CharField(blank=True, max_length=250, null=True)),
                ('ert', models.CharField(blank=True, max_length=250, null=True)),
                ('gen', models.CharField(blank=True, max_length=250, null=True)),
                ('imi', models.CharField(blank=True, max_length=250, null=True)),
                ('lin', models.CharField(blank=True, max_length=250, null=True)),
                ('mer', models.CharField(blank=True, max_length=250, null=True)),
                ('nit', models.CharField(blank=True, max_length=250, null=True)),
                ('nor', models.CharField(blank=True, max_length=250, null=True)),
                ('oxa', models.CharField(blank=True, max_length=250, null=True)),
                ('pen', models.CharField(blank=True, max_length=250, null=True)),
                ('pol', models.CharField(blank=True, max_length=250, null=True)),
                ('ppt', models.CharField(blank=True, max_length=250, null=True)),
                ('str', models.CharField(blank=True, max_length=250, null=True)),
                ('sut', models.CharField(blank=True, max_length=250, null=True)),
                ('tei', models.CharField(blank=True, max_length=250, null=True)),
                ('tet', models.CharField(blank=True, max_length=250, null=True)),
                ('van', models.CharField(blank=True, max_length=250, null=True)),
            ],
        ),
    ]