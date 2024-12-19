from rest_framework import serializers
from .models import Genre, Movie, Actor, Movie_Actor

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'

class Movie_ActorSerializer(serializers.ModelSerializer):
    id_actor = ActorSerializer()
    character = serializers.CharField()
    class Meta:
        model = Movie_Actor
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    actors = Movie_ActorSerializer(source='movie_actor_set', many=True)
    genres = GenreSerializer(many=True)

    class Meta:
        model = Movie
        fields = '__all__'