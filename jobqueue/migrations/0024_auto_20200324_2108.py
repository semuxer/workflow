# Generated by Django 3.0 on 2020-03-24 19:08

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('jobqueue', '0023_tagtype_color'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='jobs',
            managers=[
                ('tagged', django.db.models.manager.Manager()),
            ],
        ),
    ]
