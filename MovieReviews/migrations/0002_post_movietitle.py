# Generated by Django 4.1.3 on 2022-12-04 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MovieReviews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='movieTitle',
            field=models.CharField(default='not defined', max_length=200),
        ),
    ]