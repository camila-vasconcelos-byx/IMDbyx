from django.test import TestCase
from IMDbyx.models import CustomUser
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.messages import get_messages

# Create your tests here.

class ViewsTestCase(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            email= 'camila@gmail.com',
            password= 'senha',
            name= 'Camila'
        )

    def test_user_login_correct(self):
        data = {
            'email': 'camila@gmail.com',
            'password': 'senha'
        }
        response = self.client.post(reverse('user-login'), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('list-movies'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_user_login_incorrect(self):
        data = {
            'email': 'camila@gmail.com',
            'password': 'errado'
        }

        response = self.client.post(reverse('user-login'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user-login'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'There was an error logging in!')

    def test_user_login_load_page(self):
        response = self.client.get(reverse('user-login'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_user_login_no_data(self):
        data = {
            'email': '',
            'password': ''
        }
        response = self.client.post(reverse('user-login'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user-login'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'There was an error logging in!')

    def create_user_correct(self):
        data = {
            'email': 'gabriel@gmail.com',
            'password': 'senha',
            'name': 'Gabriel'
        }

        response = self.client.post(reverse('create-user'), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('list-movies'))

        user = response.wsgi_request.user
        self.assertTrue(user.is_authenticated)
        self.assertFalse(user.is_superuser)

    def create_user_repeated(self):
        data = {
            'email': 'camila@gmail.com',
            'password': 'senha',
            'name': 'Gabriel'
        }
        response = self.client.post(reverse('create-user'), data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/create_user.html')

        form = response.content['form']
        self.assertTrue(form.errors)
        self.assertContains(response, 'email: An user with this email already exists.')
