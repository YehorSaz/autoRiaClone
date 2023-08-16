# Generated by Django 4.2.4 on 2023-08-09 09:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_alter_postmodel_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='postmodel',
            name='views_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='postmodel',
            name='price',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100000000)]),
        ),
    ]