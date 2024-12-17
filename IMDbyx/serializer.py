from rest_framework import serializers
from .models import Genre, Movie, Actor, Movie_Actor

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'

class Movie_ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie_Actor
        fields = '__all__'