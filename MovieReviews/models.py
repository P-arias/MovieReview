from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):

    details = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    authorId = models.ForeignKey(User, on_delete=models.CASCADE)
    movieId = models.CharField(max_length=200)
    movieTitle = models.CharField(max_length=200)
    def __str__(self):
        return self.description

class SearchTerms(models.Model):

    term = models.CharField(max_length=200)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.description

