# Generated by Django 4.2.4 on 2023-08-09 15:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0003_alter_carmodel_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carmodel',
            name='post',
        ),
    ]
