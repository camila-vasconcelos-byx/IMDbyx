from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework import status
import requests
from .models import Genre, Movie, Actor, Movie_Actor, CustomUser
from .serializer import GenreSerializer, MovieSerializer, ActorSerializer, Movie_ActorSerializer
from rest_framework.pagination import PageNumberPagination
from django.contrib import messages
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# Create your views here.

@api_view(['GET'])
def get_api_info(request):
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

    for i in range(1, 100):
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
    paginator = PageNumberPagination()
    paginator.page_size = 24
    result = paginator.paginate_queryset(movies, request)
    serializer = MovieSerializer(result, many=True)

    genres = Genre.objects.all()
    serializer_genre = GenreSerializer(genres, many=True)

    return render(request, 'IMDbyx/index.html', {
        'status': status.HTTP_200_OK,
        'movies': serializer.data,
        'page': paginator.page.number,
        'total_pages': paginator.page.paginator.num_pages,
        'search': False,
        'genres': serializer_genre.data,
        'selected_genres': []
    })

@api_view(['GET'])
def list_actors(request):
    actors = Actor.objects.all()

    paginator = PageNumberPagination()
    paginator.page_size = 24
    result = paginator.paginate_queryset(actors, request)
    serializer = ActorSerializer(result, many=True)

    return render(request, 'IMDbyx/list_actors.html', {
        'actors': serializer.data,
        'page': paginator.page.number,
        'total_pages': paginator.page.paginator.num_pages,
    })

@api_view(['GET'])
def list_cast(request):
    cast = Movie_Actor.objects.all()
    serializer = Movie_ActorSerializer(cast, many=True)

    return Response({'message':'OK', 'cast': serializer.data})

@api_view(['GET'])
def list_genres(request):
    genres = Genre.objects.all()
    serializer = GenreSerializer(genres, many=True)

    return Response({'message':'OK', 'genres': serializer.data})

@api_view(['GET'])
def info_movie(request, id):
    movie = get_object_or_404(Movie, id=id)
    serializer = MovieSerializer(movie)

    year = movie.release_date.year

    user = request.user
    is_favorite = False
    is_watchlist = False

    if user.is_authenticated:
        is_favorite = user.favorite_movies.filter(id=id).exists()
        is_watchlist = user.watch_list.filter(id=id).exists()

    return render(request, 'IMDbyx/movie_details.html', {
        'movie': serializer.data,
        'year': year,
        'is_favorite': is_favorite,
        'is_watchlist': is_watchlist
    })

@api_view(['GET'])
def filter_genre(request):
    genres = request.GET.getlist('genres') 

    year = request.GET.get('year')
    actor = request.GET.get('actor')
    
    movies = Movie.objects.all()

    if genres:
        for genre in genres:
            movies = movies.filter(genres__id = genre)
    if year:
        movies = movies.filter(release_date__year = int(year))
    
    if actor:
        movies = movies.filter(actors__name__icontains=actor)

    if not len(movies):
        messages.success(request, ('No movies match the genre id specified.'))
        return redirect('list-movies')
           
    paginator = PageNumberPagination()
    paginator.page_size = 24
    result = paginator.paginate_queryset(movies, request)
    serializer = MovieSerializer(result, many=True)

    return render(request, 'IMDbyx/index.html', {
        'movies': serializer.data,
        'search': False,
        'genres': GenreSerializer(Genre.objects.all(), many=True).data,
        'selected_genres': [int(id) for id in genres],
        'status': status.HTTP_200_OK,
        'page': paginator.page.number,
        'total_pages': paginator.page.paginator.num_pages,
    })

@api_view(['GET'])
def search_movies(request):
    movie_name = request.GET.get('movie', '').strip()

    if not movie_name:
        messages.success(request, ('You must type a movie title.'))
        return redirect('list-movies')
    
    movies = Movie.objects.filter(title__contains=movie_name)

    if len(movies) == 0:
        messages.success(request, (f'No movie matches the search "{movie_name}".'))
        return redirect('list-movies')
    else:
        messages.success(request, (f'{len(movies)} results were found for the search "{movie_name}"!'))

    paginator = PageNumberPagination()
    paginator.page_size = 24
    result = paginator.paginate_queryset(movies, request)
    serializer = MovieSerializer(result, many=True)

    return render(request, 'IMDbyx/index.html', {
        'status': status.HTTP_200_OK,
        'movies': serializer.data,
        'search': True,
        'page': paginator.page.number,
        'total_pages': paginator.page.paginator.num_pages,
    })

@login_required
def add_to_favorites(request, id):
    movie = get_object_or_404(Movie, id=id) 
    user = request.user

    if user.favorite_movies.filter(id = id).exists():
        messages.success(request, ('This movie has already been added to your favorites!'))
    else:
        user.favorite_movies.add(movie)
        messages.success(request, ('Movie added to favorites!'))
    
    if user.watch_list.filter(id=id).exists():
        return remove_watchlist(request, id)

    return redirect('movie-details', id=id)

@login_required
@api_view(['GET'])
def view_favorites(request):
    user = request.user
    
    movies = user.favorite_movies.all()

    paginator = PageNumberPagination()
    paginator.page_size = 24
    result = paginator.paginate_queryset(movies, request)
    serializer = MovieSerializer(result, many=True)

    sentence = f"{user.name}'s Favorite Movies"

    return render(request, 'IMDbyx/favorite_movies.html', {
        'movies': serializer.data,
        'sentence': sentence,
        'page': paginator.page.number,
        'total_pages': paginator.page.paginator.num_pages,
    })

@login_required
def remove_favorites(request, id):
    user = request.user
    movie = get_object_or_404(Movie, id=id)
    user.favorite_movies.remove(movie)

    messages.success(request, ('Movie removed from favorites.'))
    return redirect('movie-details', id=id)

@login_required
def add_to_watchlist(request, id):
    movie = get_object_or_404(Movie, id=id)
    user = request.user

    if user.watch_list.filter(id = id).exists():
        messages.success(request, ('This movie has already been added to your WatchList!'))
    else:
        user.watch_list.add(movie)
        messages.success(request, ('Movie added to WatchList!'))

    return redirect('movie-details', id=id)

@login_required
@api_view(['GET'])
def view_watchlist(request):
    user = request.user
    
    movies = user.watch_list.all()

    paginator = PageNumberPagination()
    paginator.page_size = 24
    result = paginator.paginate_queryset(movies, request)
    serializer = MovieSerializer(result, many=True)

    sentence = f"{user.name}'s Watchlist"

    return render(request, 'IMDbyx/favorite_movies.html', {
            'movies': serializer.data,
            'sentence': sentence,
            'page': paginator.page.number,
            'total_pages': paginator.page.paginator.num_pages,
        })

@login_required
def remove_watchlist(request, id):
    user = request.user
    movie = get_object_or_404(Movie, id=id)
    user.watch_list.remove(movie)

    messages.success(request, ('Movie removed from WatchList.'))
    return redirect('movie-details', id=id)

@api_view(['GET'])
def actor_details(request, id):
    actor = get_object_or_404(Actor, id=id)
    actor_serializer = ActorSerializer(actor)

    movies = actor.movies.all()
    serializer = MovieSerializer(movies, many=True)

    return render(request, 'IMDbyx/actor_details.html', {
        'actor': actor_serializer.data,
        'movies': serializer.data
    })

@api_view(['GET'])
def search_actors(request): 
    actor_name = request.GET.get('actor', '').strip()

    if not actor_name:
        messages.success(request, ('You must type an actor name.'))
        return redirect('list-actors')
    
    actors = Actor.objects.filter(name__icontains = actor_name)

    if len(actors) == 0:
        messages.success(request, (f'No actor matches the search "{actor_name}".'))
        return redirect('list-actors')
    else:
        messages.success(request, (f'{len(actors)} results were found for the search "{actor_name}"!'))

    paginator = PageNumberPagination()
    paginator.page_size = 24
    result = paginator.paginate_queryset(actors, request)
    serializer = ActorSerializer(result, many=True)

    return render(request, 'IMDbyx/list_actors.html', {
        'actors': serializer.data,
        'page': paginator.page.number,
        'total_pages': paginator.page.paginator.num_pages,
    })

def set_page_choice(request, choice):
    if choice in ['movies', 'actors']:  
        request.session['page_choice'] = choice 
    
    if choice == 'actors':
        return redirect('list-actors')
    return redirect('list-movies')