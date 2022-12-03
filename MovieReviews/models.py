from django.db import models

# Create your models here.
class Post(models.Model):
    details = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    movieId = models.CharField(max_length=200)

    def __str__(self):
        return self.description
