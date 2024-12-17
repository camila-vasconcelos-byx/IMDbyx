import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_genres(api_key):
        url = 'https://api.themoviedb.org/3/genre/movie/list'

        params = {
                'api_key': api_key
        }

        response = requests.get(url, params=params, verify=False)
        response = response.json().get('genres')
        genres = {genre['id']: genre['name'] for genre in response}

        return genres

def get_similar_movies(movie_id, api_key):
        url = f'https://api.themoviedb.org/3/movie/{movie_id}/similar'

        params = {
                'api_key': api_key
        }

        response = requests.get(url, params=params, verify=False)
        response = response.json().get('results')

        similar = response[:5]
        similar = [movie['id'] for movie in similar]
        
        return similar

def get_cast_movie(movie_id, api_key):
        url = f'https://api.themoviedb.org/3/movie/{movie_id}/credits'

        params = {
                'api_key': api_key
        }

        response = requests.get(url, params=params, verify=False)
        response = response.json().get('cast')
        actors = response[:5]
        actors = [{key: actor[key] for key in ['id', 'name', 'profile_path', 'character']} for actor in actors]
        
        return actors

api_key = '7e12595b713f21bd5212e899661d80cf'
all_genres = get_genres(api_key)


url = 'https://api.themoviedb.org/3/discover/movie'

params = {
        "api_key": api_key,
        "page": 1 
}

response = requests.get(url, params=params, verify=False)
response = response.json()

img_url = "http://image.tmdb.org/t/p/"

for movie in response.get('results'):
        title = movie['title']
        id = movie['id']
        url_poster = img_url + 'w185' + movie['poster_path']
        url_path = img_url + 'original' + movie['backdrop_path']
        overview = movie['overview']
        release_date = movie['release_date']
        genres = movie['genre_ids']
        genres = [all_genres[genre] for genre in genres]
        similar_movies = get_similar_movies(id, api_key)
        cast = get_cast_movie(id, api_key)
        print(title)
        print(id)
        print(genres)
        print(url_poster)
        print(url_path)
        print(similar_movies)
        print(cast)
        print()
