# Generated by Django 2.1 on 2020-02-20 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dataemail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('message', models.CharField(max_length=100)),
                ('from_email', models.EmailField(max_length=254)),
            ],
        ),
    ]