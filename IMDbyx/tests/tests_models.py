from django.test import TestCase
from ..models import Movie, Genre, Actor, Movie_Actor

class ModelsTestCase(TestCase):
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

        actor1 = Actor.objects.create(id=1, name="Leonardo DiCaprio")
        actor2 = Actor.objects.create(id=2, name="Joseph Gordon-Levitt")

        Movie_Actor.objects.create(id_movie=movie1, id_actor=actor1, character="Dom Cobb")
        Movie_Actor.objects.create(id_movie=movie1, id_actor=actor2, character="Arthur")
        Movie_Actor.objects.create(id_movie=movie2, id_actor=actor1, character="Cooper")
