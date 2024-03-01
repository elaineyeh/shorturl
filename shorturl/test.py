from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APIClient

from http import HTTPStatus

from .models import Url


class ShortUrlTests(TestCase):
    def setUp(self):
        user = User.objects.create(username='test', password='test', email='test@test.com')
        self.client = APIClient()
        self.client.force_login(user=user)

        self.anonymous_client = APIClient()

        self.shorturl = Url.objects.create(url='https://google.com', code='test')

    def create_shorturl(self, client):
        response = client.post('/', data={'url': 'https://test.com', 'code': 'abcd'})
        return response

    def redirect_url(self, client, code):
        response = client.get(reverse('shorturl:redirct_url', kwargs={'code': self.shorturl.code}))
        return response

    def test_user_can_generate_shorturl(self):
        response = self.create_shorturl(self.client)

        self.assertEqual(response.context['code'].code, 'abcd')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_can_generate_shorturl_without_code(self):
        response = self.client.post('/', data={'url': 'https://test.com'})

        self.assertEqual(response.context['code'].code, Url.objects.get(id=response.context['code'].id).code)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_anonymous_can_not_generate_shorturl(self):
        response = self.create_shorturl(self.anonymous_client)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, '/account/login/?next=/')

    def test_user_can_redirect_from_shorturl_to_original_url(self):
        response = self.redirect_url(self.client, self.shorturl.code)

        self.assertEqual(response.status_code, status.HTTP_301_MOVED_PERMANENTLY)
        self.assertEqual(response['Location'], self.shorturl.url)


