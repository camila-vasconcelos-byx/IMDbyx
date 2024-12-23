from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

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
    popularity = models.FloatField(null=True)
    vote = models.FloatField(null=True)

class Movie_Actor(models.Model):
    id_movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    id_actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    character = models.CharField(max_length=100)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The user must have an email.')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        if password:
            user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, null=True)
    favorite_movies = models.ManyToManyField(Movie, related_name='favorite_movies')
    watch_list = models.ManyToManyField(Movie, related_name='watch_list')
    watched_movies = models.ManyToManyField(Movie, related_name='watched_movies')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()
    