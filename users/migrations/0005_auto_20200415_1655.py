# Generated by Django 2.1 on 2020-04-15 16:55

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20200402_2302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=cloudinary.models.CloudinaryField(default='v1586706164/defaultNew.png', max_length=255, verbose_name='image'),
        ),
    ]