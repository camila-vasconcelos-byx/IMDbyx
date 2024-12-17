from django.db import models

# Create your models here.

class Genre(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)

class Actor(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    image_path = models.CharField(max_length=255)

class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    overview = models.TextField()
    release_date = models.DateField()
    image_poster = models.CharField(max_length=255)
    image_backdrop = models.CharField(max_length=255)
    actors = models.ManyToManyField(Actor, related_name='movies', through='Movie_Actor')
    genres = models.ManyToManyField(Genre, related_name='genres')

class Movie_Actor(models.Model):
    id_movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    id_actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    character = models.CharField(max_length=100)