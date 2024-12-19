from django.urls import path
from . import views 

urlpatterns = [
    path('', views.list_movies, name='index'),
    path('update-bd', views.get_api_info, name='get-api-info'),
    path('', views.list_movies, name='list-movies'),
    path('list-actors', views.list_actors, name='list-actors'),
    path('list-cast', views.list_cast, name='list-cast'),
    path('list-genres', views.list_genres, name='list-genres'),
    path('movie-details/<id>', views.info_movie, name='movie-details'),
    path('genre/<genre>', views.filter_genre, name='filter-genre'),
    path('search', views.search_movies, name='search-movies'),
    # path('<movie>', views.movie_detail, name='movie-detail'),
]
