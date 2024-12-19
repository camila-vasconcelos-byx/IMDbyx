from django.test import TestCase
from .models import Genre


class AnimalTestCase(TestCase):
    def setUp(self):
        Genre.objects.create(name="lion", id=123)
        Genre.objects.create(name="cat", id=234)

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        lion = Genre.objects.filter(name="lion").first()
        dog = Genre.objects.filter(name="cat").first()
        self.assertIsInstance(lion, Genre)
        self.assertIsInstance(dog, Genre)

