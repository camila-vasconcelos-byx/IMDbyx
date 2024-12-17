from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name='index'),
    path('update-bd', views.get_api_info, name='get-api-info'),
    path('list-movies', views.list_movies, name='list-movies'),
    path('list-actors', views.list_actors, name='list-actors'),
    path('list-cast', views.list_cast, name='list-cast'),
    path('movie-details/<id>', views.info_movie, name='movie-details'),
    path('genre/<genre>', views.filter_genre, name='filter-genre'),
    path('search/<movie_name>', views.search_movies, name='search-movies'),
    path('<movie>', views.movie_detail, name='movie-detail'),
]
