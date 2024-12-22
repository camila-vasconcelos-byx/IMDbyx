from django.urls import path
from . import views 

urlpatterns = [
    path('', views.list_movies, name='list-movies'),
    path('update-bd', views.get_api_info, name='get-api-info'),
    path('list-actors', views.list_actors, name='list-actors'),
    path('list-cast', views.list_cast, name='list-cast'),
    path('list-genres', views.list_genres, name='list-genres'),
    path('movie-details/<id>', views.info_movie, name='movie-details'),
    path('genre', views.filter_genre, name='filter-genre'),
    path('search', views.search_movies, name='search-movies'),
    path('add-to-favorites/<id>', views.add_to_favorites, name='add-to-favorites'),
    path('view-favorites', views.view_favorites, name='view-favorites'),
    path('remove-from-favorites/<id>', views.remove_favorites, name='remove-from-favorites'),
    path('add-to-watchlist/<id>', views.add_to_watchlist, name='add-to-watchlist'),
    path('view-watchlist', views.view_watchlist, name='view-watchlist'),
    path('remove-from-watchlist/<id>', views.remove_watchlist, name='remove-from-watchlist')
]
