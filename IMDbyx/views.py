from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests
from .models import Genre, Movie, Actor, Movie_Actor
from .serializer import GenreSerializer, MovieSerializer, ActorSerializer, Movie_ActorSerializer
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# Create your views here.

def index(request):
    return render(request, 'IMDbyx/index.html')

def movie_detail(request, movie):
    return render(request, 'IMDbyx/movie.html')

@api_view(['GET'])
def get_api_info(request):
    print('aqui')
    api_key = '7e12595b713f21bd5212e899661d80cf'

    def get_genres():
        url = 'https://api.themoviedb.org/3/genre/movie/list'

        params = {
                'api_key': api_key
        }

        response = requests.get(url, params=params, verify=False)
        response = response.json().get('genres')
        for genre in response:
            _ = Genre.objects.update_or_create(
                id = genre['id'],
                defaults={
                    'name': genre['name']
                }
            )

    def get_cast(movie_id, filme):
        url = f'https://api.themoviedb.org/3/movie/{movie_id}/credits'

        params = {
                'api_key': api_key
        }

        response = requests.get(url, params=params, verify=False)
        response = response.json().get('cast')
        actors = response[:5]

        for actor in actors:
            id_actor = actor['id']
            name = actor['name']
            image_profile = actor['profile_path']
            character = actor['character']

            try:
                ator, _ = Actor.objects.update_or_create(
                    id = id_actor,
                    defaults={
                        'name': name,
                        'image_path': image_profile
                    }
                )

                _ = Movie_Actor.objects.update_or_create(
                    id_actor = ator,
                    id_movie = filme,
                    character = character
                )
            except:
                return Response({'message': 'Algo deu errado!'})
                
    get_genres()
    genres = Genre.objects.all()

    url = 'https://api.themoviedb.org/3/discover/movie'

    for i in range(1, 5):
        print(i)
        params = {
                "api_key": api_key,
                "page": i 
        }

        response = requests.get(url, params=params, verify=False)
        response = response.json()

        for movie in response.get('results'):
            title = movie['title']
            id_movie = movie['id']
            url_poster = movie['poster_path']
            url_backdrop = movie['backdrop_path']
            overview = movie['overview']
            release_date = movie['release_date']
            genre_ids = movie['genre_ids']
            genres = Genre.objects.filter(id__in=genre_ids)

            try:
                filme, _ = Movie.objects.update_or_create(
                    id = id_movie, 
                    defaults={
                        'title': title,
                        'overview': overview,
                        'release_date': release_date,
                        'image_poster': url_poster,
                        'image_backdrop': url_backdrop,
                    }
                )

                filme.genres.set(genres)
                get_cast(id_movie, filme)
            except:
                continue

    movies = Movie.objects.all()
    # serializer = MovieSerializer(movies, many=True)
    return Response({'message': 'filmes adicionados com sucesso!', 'movies': len(movies)})

@api_view(['GET'])
def list_movies(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)

    return Response({'message': 'OK', 'movies': serializer.data})

@api_view(['GET'])
def list_actors(request):
    actors = Actor.objects.all()
    serializer = ActorSerializer(actors, many=True)

    return Response({'message':'OK', 'actors': serializer.data})

@api_view(['GET'])
def list_cast(request):
    cast = Movie_Actor.objects.all()
    serializer = Movie_ActorSerializer(cast, many=True)

    return Response({'message':'OK', 'cast': serializer.data})

@api_view(['GET'])
def info_movie(request, id):
    movie = Movie.objects.get(id=id)
    serializer = MovieSerializer(movie)

    return Response({'message': 'OK', 'movie': serializer.data})

@api_view(['GET'])
def filter_genre(request, genre):
    genre = genre.capitalize()
    try:
        id_genre = Genre.objects.get(name = genre).id
    except Genre.DoesNotExist:
        return Response({'message': 'Genre not found!'}, status.HTTP_400_BAD_REQUEST)

    movies = Movie.objects.filter(genres__id = id_genre).distinct()
    serializer = MovieSerializer(movies, many=True)

    return Response({'message': 'OK', 'movies': serializer.data})

@api_view(['GET'])
def search_movies(request, movie_name):
    movies = Movie.objects.filter(title__contains=movie_name)
    serializer = MovieSerializer(movies, many=True)

    return Response({'message': 'OK', 'movies': serializer.data})
