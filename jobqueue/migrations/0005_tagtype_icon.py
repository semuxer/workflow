# Generated by Django 3.0 on 2019-12-19 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobqueue', '0004_auto_20191219_2210'),
    ]

    operations = [
        migrations.AddField(
            model_name='tagtype',
            name='icon',
            field=models.CharField(choices=[('&#xe84d;', '<i class="material-icons">&#xe84d;</i>'), ('&#xeb3b;', '<i class="material-icons">&#xeb3b;</i>'), ('&#xe190;', '<i class="material-icons">&#xe190;</i>')], db_index=True, default='СТАРТ', max_length=40),
        ),
    ]
