# Generated by Django 3.0 on 2019-12-23 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobqueue', '0014_auto_20191222_2109'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobs',
            name='customer',
            field=models.CharField(db_index=True, default='', max_length=255, verbose_name='Заказчик'),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='name',
            field=models.CharField(db_index=True, default='', max_length=255, verbose_name='Название работы'),
        ),
    ]