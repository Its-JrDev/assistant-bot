from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import User
from students.models import Student
from academics.models import Course


class StudentAPITest(APITestCase):
    def setUp(self):
        self.directivo = User.objects.create_user(
            username='directivo', password='admin123', role='directivo',
        )
        self.profesor = User.objects.create_user(
            username='profesor1', password='profesor123', role='profesor',
        )
        self.course_a = Course.objects.create(name='1A', academic_year=2026)
        self.course_b = Course.objects.create(name='1B', academic_year=2026)
        self.student = Student.objects.create(
            dni='12345678', pin_hash='pbkdf2_sha256$...', nombre='Test Student',
            course=self.course_a,
        )
        self.list_url = '/api/students/'

    def test_list_students(self):
        self.client.force_authenticate(user=self.directivo)
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 1)

    def test_filter_by_course(self):
        self.client.force_authenticate(user=self.directivo)
        resp = self.client.get(f'{self.list_url}?course={self.course_a.id}')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 1)

        resp = self.client.get(f'{self.list_url}?course={self.course_b.id}')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 0)

    def test_search_by_name(self):
        self.client.force_authenticate(user=self.directivo)
        resp = self.client.get(f'{self.list_url}?search=Test')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 1)

    def test_search_by_dni(self):
        self.client.force_authenticate(user=self.directivo)
        resp = self.client.get(f'{self.list_url}?search=12345678')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 1)

    def test_create_student_as_directivo(self):
        self.client.force_authenticate(user=self.directivo)
        data = {
            'dni': '87654321',
            'pin_hash': 'abc123',
            'nombre': 'New Student',
            'course': self.course_a.id,
        }
        resp = self.client.post(self.list_url, data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_create_student_as_profesor(self):
        self.client.force_authenticate(user=self.profesor)
        data = {
            'dni': '11111111',
            'pin_hash': 'abc',
            'nombre': 'Another',
            'course': self.course_a.id,
        }
        resp = self.client.post(self.list_url, data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_unauthenticated_blocked(self):
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
