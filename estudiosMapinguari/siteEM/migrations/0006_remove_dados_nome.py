# Generated by Django 2.2.3 on 2019-07-20 12:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('siteEM', '0005_dados_nome'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dados',
            name='nome',
        ),
    ]