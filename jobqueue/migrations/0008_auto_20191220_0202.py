# Generated by Django 3.0 on 2019-12-20 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobqueue', '0007_auto_20191220_0159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tagtype',
            name='icon',
            field=models.CharField(blank=True, db_index=True, default='', max_length=100, null=True, verbose_name='Иконка'),
        ),
    ]
