# Generated by Django 2.2.3 on 2019-07-22 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0002_auto_20190722_1414'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='views',
            new_name='viewscat',
        ),
    ]