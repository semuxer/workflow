# Generated by Django 3.0 on 2019-12-19 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobqueue', '0005_tagtype_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tagtype',
            name='icon',
            field=models.CharField(db_index=True, max_length=40, verbose_name='Иконка'),
        ),
    ]
