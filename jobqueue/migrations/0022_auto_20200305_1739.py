# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2020-03-05 15:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobqueue', '0021_auto_20200228_1531'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobs',
            name='info',
            field=models.CharField(blank=True, db_index=True, default='', max_length=255, null=True, verbose_name='Дополнительная информация'),
        ),
        migrations.AddField(
            model_name='jobs',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='jobqueue.Profile', verbose_name='Создал'),
        ),
        migrations.AddField(
            model_name='jobs',
            name='paper',
            field=models.CharField(blank=True, db_index=True, default='', max_length=255, null=True, verbose_name='Бумага'),
        ),
    ]