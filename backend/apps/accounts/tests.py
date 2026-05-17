from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.hashers import make_password
from accounts.models import User


class UserAPITest(APITestCase):
    def setUp(self):
        self.directivo = User.objects.create_user(
            username='directivo', password='admin123',
            role='directivo', full_name='Directivo Test',
        )
        self.profesor = User.objects.create_user(
            username='profesor1', password='profesor123',
            role='profesor', full_name='Profesor Test',
        )
        self.list_url = '/api/users/'

    def test_list_users_as_directivo(self):
        self.client.force_authenticate(user=self.directivo)
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_list_users_as_profesor_forbidden(self):
        self.client.force_authenticate(user=self.profesor)
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user_as_directivo(self):
        self.client.force_authenticate(user=self.directivo)
        data = {
            'username': 'nuevo_prof',
            'password': 'pass1234',
            'role': 'profesor',
            'full_name': 'Nuevo Prof',
        }
        resp = self.client.post(self.list_url, data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)

    def test_create_user_as_profesor_forbidden(self):
        self.client.force_authenticate(user=self.profesor)
        data = {
            'username': 'otro',
            'password': 'pass1234',
            'role': 'profesor',
        }
        resp = self.client.post(self.list_url, data)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_blocked(self):
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_as_directivo(self):
        self.client.force_authenticate(user=self.directivo)
        url = f'/api/users/{self.profesor.id}/'
        resp = self.client.patch(url, {'full_name': 'Updated Name'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.profesor.refresh_from_db()
        self.assertEqual(self.profesor.full_name, 'Updated Name')

    def test_delete_user_as_profesor_forbidden(self):
        self.client.force_authenticate(user=self.profesor)
        url = f'/api/users/{self.directivo.id}/'
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
