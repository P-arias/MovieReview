# Generated by Django 4.1.3 on 2022-12-03 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('details', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=200)),
                ('movieId', models.CharField(max_length=200)),
            ],
        ),
    ]
