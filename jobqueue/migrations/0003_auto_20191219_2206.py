# Generated by Django 3.0 on 2019-12-19 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobqueue', '0002_auto_20191218_0709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tagtype',
            name='name',
            field=models.CharField(db_index=True, default='', max_length=128, verbose_name='Название тега'),
        ),
    ]
