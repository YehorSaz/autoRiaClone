# Generated by Django 4.2.4 on 2023-08-09 15:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_remove_postmodel_brand_remove_postmodel_images_and_more'),
        ('cars', '0002_alter_carmodel_brand_alter_carmodel_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carmodel',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='car', to='posts.postmodel'),
        ),
    ]
