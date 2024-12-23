from django.test import TestCase
from ..models import Genre, Movie, Actor, Movie_Actor
from ..serializer import MovieSerializer, ActorSerializer
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth import get_user_model

class ViewsTesteCase(TestCase):
    def setUp(self):
        movie1 = Movie.objects.create(
            id=1,
            title="Inception",
            overview="A skilled thief is offered a chance to erase his past crimes.",
            release_date="2010-07-16",
            image_poster="inception-poster.jpg",
            image_backdrop="inception-backdrop.jpg",
        )
        movie2 = Movie.objects.create(
            id=2,
            title="Interstellar",
            overview="A team of explorers travel through a wormhole in space.",
            release_date="2014-11-07",
            image_poster="interstellar-poster.jpg",
            image_backdrop="interstellar-backdrop.jpg",
        )

        genre1 = Genre.objects.create(id=1, name="Action")
        genre2 = Genre.objects.create(id=2, name="Sci-Fi")
        genre3 = Genre.objects.create(id=3, name='Fantasy')

        movie1.genres.add(genre1)
        movie1.genres.add(genre2)
        movie2.genres.add(genre1)
        movie2.genres.add(genre3)

        user = get_user_model().objects.create_user(
            email= 'camila@gmail.com',
            password= 'senha',
            name= 'Camila'
        )

        user.favorite_movies.add(movie2)

        actor1 = Actor.objects.create(id=1, name="Leonardo DiCaprio")
        actor2 = Actor.objects.create(id=2, name="Joseph Gordon-Levitt")
        actor3 = Actor.objects.create(id=3, name="Matthew McConaughey")
        actor4 = Actor.objects.create(id=4, name="Anne Hathaway")

        Movie_Actor.objects.create(id_actor=actor1, id_movie=movie1, character="Cobb")
        Movie_Actor.objects.create(id_actor=actor2, id_movie=movie1, character="Arthur")

        Movie_Actor.objects.create(id_actor=actor3, id_movie=movie2, character="Cooper")
        Movie_Actor.objects.create(id_actor=actor4, id_movie=movie2, character="Brand")


    def test_list_movies_200_response(self):
        response = self.client.get(reverse('list-movies'))
        self.assertEqual(response.status_code, 200)

    def test_list_movies_template(self):
        response = self.client.get(reverse('list-movies'))
        self.assertTemplateUsed(response, 'IMDbyx/index.html')

    def test_list_movies(self):
        response = self.client.get(reverse('list-movies'))
        response_movies = response.context['movies']

        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        self.assertEqual(response_movies, serializer.data)

    def test_movie_details_200_response(self):
        response = self.client.get(reverse('movie-details', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 200)

    def test_movie_details_template(self):
        response = self.client.get(reverse('movie-details', kwargs={'id': 1}))
        self.assertTemplateUsed(response, 'IMDbyx/movie_details.html')

    def test_movie_details_404_response(self):
        response = self.client.get(reverse('movie-details', kwargs={'id': 5}))
        self.assertEqual(response.status_code, 404)

    def test_filter_genres_200_response(self):
        response = self.client.get(reverse('filter-genre'), {'genres': [1]})
        self.assertEqual(response.status_code, 200)

    def test_filter_genres_template(self):
        response = self.client.get(reverse('filter-genre'), {'genres': [1]})
        self.assertTemplateUsed(response, 'IMDbyx/index.html')

    def test_filter_genres(self):
        response = self.client.get(reverse('filter-genre'), {'genres': [1]})
        response_movies = response.context['movies']

        movies = Movie.objects.filter(genres__id=1)
        serializer = MovieSerializer(movies, many=True)

        self.assertEqual(response_movies, serializer.data)

    def test_filter_genres_dont_exist(self):
        response = self.client.get(reverse('filter-genre'), {'genres':[5]})
        
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(str(messages[0]), 'No movies match the filter specified.')
        self.assertRedirects(response, reverse('list-movies'))

    def test_filter_genres_no_match(self):
        response = self.client.get(reverse('filter-genre'), {'genres':[1,2,3]})
        
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(str(messages[0]), 'No movies match the filter specified.')
        self.assertRedirects(response, reverse('list-movies'))

    def test_search_movie_200_response(self):
        response = self.client.get(reverse('search-movies') + '?movie= Inception ')
        self.assertEqual(response.status_code, 200)

    def test_search_movie_template(self):
        response = self.client.get(reverse('search-movies') + '?movie= Inception ')
        self.assertTemplateUsed(response, 'IMDbyx/index.html')

    def test_search_movie_no_parameters(self):
        response = self.client.get(reverse('search-movies'))

        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('list-movies'))
        self.assertEqual(str(messages[0]), 'You must type a movie title.')

    def test_search_movie_found(self):
        response = self.client.get(reverse('search-movies') + '?movie= In ')

        self.assertEqual(response.status_code, 200)

        response_movies = response.context['movies']

        movies = Movie.objects.filter(title__contains = 'In')
        serializer = MovieSerializer(movies, many=True)

        self.assertEqual(response_movies, serializer.data)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), '2 results were found for the search "In"!')

    def test_search_movie_not_found(self):
        response = self.client.get(reverse('search-movies') + '?movie= Mamma Mia! ')

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('list-movies'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'No movie matches the search "Mamma Mia!".')

    def test_add_to_favorites_not_logged_in(self):
        response = self.client.get(reverse('add-to-favorites', kwargs={'id': 1}))

        url =  f"{reverse('user-login')}?next={reverse('add-to-favorites', kwargs={'id':1})}"

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, url)

    def test_add_to_favorites_logged_in(self):
        self.client.login(email='camila@gmail.com', password='senha')
        response = self.client.get(reverse('add-to-favorites', kwargs={'id':1}))
        user = response.wsgi_request.user

        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Movie added to favorites!')

        self.assertIn(Movie.objects.get(id=1), user.favorite_movies.all())

    def test_add_to_favorites_repeated_movie(self):
        self.client.login(email='camila@gmail.com', password='senha')
        response = self.client.get(reverse('add-to-favorites', kwargs={'id':2}))
        user = response.wsgi_request.user

        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'This movie has already been added to your favorites!')

        self.assertIn(Movie.objects.get(id=2), user.favorite_movies.all())

    def test_add_to_favorites_invalid_id(self):
        self.client.login(email='camila@gmail.com', password='senha')
        response = self.client.get(reverse('add-to-favorites', kwargs={'id':5}))

        self.assertEqual(response.status_code, 404)

    def test_view_favorites_not_logged_in(self):
        response = self.client.get(reverse('view-favorites'))

        url =  f"{reverse('user-login')}?next={reverse('view-favorites')}"

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, url)

    def test_remove_from_favorites_not_logged_in(self):
        response = self.client.get(reverse('remove-from-favorites', kwargs={'id': 1}))

        url =  f"{reverse('user-login')}?next={reverse('remove-from-favorites', kwargs={'id':1})}"

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, url)

    def test_remove_from_favorites_logged_in(self):
        self.client.login(email='camila@gmail.com', password='senha')
        response = self.client.get(reverse('remove-from-favorites', kwargs={'id':2}))
        user = response.wsgi_request.user

        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Movie removed from favorites.')

        self.assertNotIn(Movie.objects.get(id=2), user.favorite_movies.all())

    def test_remove_from_favorites_invalid_id(self):
        self.client.login(email='camila@gmail.com', password='senha')
        response = self.client.get(reverse('remove-from-favorites', kwargs={'id':1}))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Movie not in favorites.')

        self.assertEqual(response.status_code, 302)

    def test_remove_from_favorites_unexisting_id(self):
        self.client.login(email='camila@gmail.com', password='senha')
        response = self.client.get(reverse('remove-from-favorites', kwargs={'id':3}))

        self.assertEqual(response.status_code, 404)

    def test_list_actors_200_response(self):
        response = self.client.get(reverse('list-actors'))
        self.assertEqual(response.status_code, 200)

    def test_list_actors_template(self):
        response = self.client.get(reverse('list-actors'))
        self.assertTemplateUsed(response, 'IMDbyx/list_actors.html')

    def test_list_actors(self):
        response = self.client.get(reverse('list-actors'))
        response_actors = response.context['actors']

        actors = Actor.objects.all()
        serializer = ActorSerializer(actors, many=True)

        self.assertEqual(response_actors, serializer.data)

    def test_actor_details_200_response(self):
        response = self.client.get(reverse('actor-details', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 200)

    def test_actor_details_template(self):
        response = self.client.get(reverse('actor-details', kwargs={'id': 1}))
        self.assertTemplateUsed(response, 'IMDbyx/actor_details.html')

    def test_actor_details_correct(self):
        response = self.client.get(reverse('actor-details', kwargs={'id': 1}))
        response_actor = response.context['actor']

        actor = Actor.objects.get(id=1)
        serializer = ActorSerializer(actor)

        self.assertEqual(response_actor, serializer.data)

    def test_actor_details_invalid(self):
        response = self.client.get(reverse('actor-details', kwargs={'id': 10}))
        self.assertEqual(response.status_code, 404)

    def test_search_actors_200_response(self):
        response = self.client.get(reverse('search-actors') + '?actor= Leonardo ')
        self.assertEqual(response.status_code, 200)

    def test_search_actors_template(self):
        response = self.client.get(reverse('search-actors') + '?actor= Leonardo ')
        self.assertTemplateUsed(response, 'IMDbyx/list_actors.html')

    def test_search_actors_found(self):
        response = self.client.get(reverse('search-actors') + '?actor= Le ')
        response_actors = response.context['actors']

        actors = Actor.objects.filter(name__icontains='Le')
        serializer = ActorSerializer(actors, many=True)

        self.assertEqual(response_actors, serializer.data)
        self.assertEqual(response.status_code, 200)

        messages = list(get_messages(response.wsgi_request))
        message = '2 results were found for the search "Le"!'

        self.assertEqual(str(messages[0]), message)

    def test_search_actors_no_param(self):
        response = self.client.get(reverse('search-actors'))

        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'You must type an actor name.')

    def test_search_actors_not_found(self):
        response = self.client.get(reverse('search-actors') + '?actor= Meryl Streep ')

        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'No actor matches the search "Meryl Streep".')
