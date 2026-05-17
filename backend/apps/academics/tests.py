from datetime import date, time, timedelta
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import User
from students.models import Student
from academics.models import Course, TeacherAssignment, Schedule, Task, Event, Grade


class CourseAPITest(APITestCase):
    def setUp(self):
        self.directivo = User.objects.create_user(
            username='directivo', password='admin123', role='directivo',
        )
        self.profesor = User.objects.create_user(
            username='profesor1', password='profesor123', role='profesor',
        )
        self.course = Course.objects.create(name='1A', academic_year=2026)
        self.list_url = '/api/courses/'

    def test_list_courses(self):
        self.client.force_authenticate(user=self.directivo)
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create_course_as_directivo(self):
        self.client.force_authenticate(user=self.directivo)
        resp = self.client.post(self.list_url, {'name': '2B', 'academic_year': 2026})
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_create_course_as_profesor_forbidden(self):
        self.client.force_authenticate(user=self.profesor)
        resp = self.client.post(self.list_url, {'name': '2C', 'academic_year': 2026})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_search_course(self):
        self.client.force_authenticate(user=self.directivo)
        resp = self.client.get(f'{self.list_url}?search=1A')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 1)


class TeacherAssignmentAPITest(APITestCase):
    def setUp(self):
        self.directivo = User.objects.create_user(
            username='directivo', password='admin123', role='directivo',
        )
        self.profesor = User.objects.create_user(
            username='profesor1', password='profesor123', role='profesor',
        )
        self.course = Course.objects.create(name='1A', academic_year=2026)
        self.assignment = TeacherAssignment.objects.create(
            teacher=self.profesor, course=self.course, subject='Matemática',
        )
        self.list_url = '/api/assignments/'

    def test_list_assignments(self):
        self.client.force_authenticate(user=self.directivo)
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 1)

    def test_filter_by_teacher(self):
        self.client.force_authenticate(user=self.directivo)
        resp = self.client.get(f'{self.list_url}?teacher={self.profesor.id}')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 1)

    def test_filter_by_course(self):
        self.client.force_authenticate(user=self.directivo)
        resp = self.client.get(f'{self.list_url}?course={self.course.id}')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 1)


class ScheduleAPITest(APITestCase):
    def setUp(self):
        self.directivo = User.objects.create_user(
            username='directivo', password='admin123', role='directivo',
        )
        self.profesor = User.objects.create_user(
            username='profesor1', password='profesor123', role='profesor',
        )
        self.course = Course.objects.create(name='1A', academic_year=2026)
        self.schedule = Schedule.objects.create(
            course=self.course, day='Lunes',
            start_time=time(8, 0), end_time=time(9, 0),
            subject='Matemática',
        )
        self.list_url = '/api/schedules/'

    def test_list_schedules(self):
        self.client.force_authenticate(user=self.directivo)
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 1)

    def test_filter_by_course(self):
        self.client.force_authenticate(user=self.directivo)
        resp = self.client.get(f'{self.list_url}?course={self.course.id}')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 1)

    def test_filter_by_day(self):
        self.client.force_authenticate(user=self.directivo)
        resp = self.client.get(f'{self.list_url}?day=Lunes')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 1)

        resp = self.client.get(f'{self.list_url}?day=Martes')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 0)

    def test_create_schedule_as_profesor_forbidden(self):
        self.client.force_authenticate(user=self.profesor)
        data = {
            'course': self.course.id, 'day': 'Martes',
            'start_time': '10:00', 'end_time': '11:00',
            'subject': 'Lengua',
        }
        resp = self.client.post(self.list_url, data)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)


class TaskAPITest(APITestCase):
    def setUp(self):
        self.directivo = User.objects.create_user(
            username='directivo', password='admin123', role='directivo',
        )
        self.profesor = User.objects.create_user(
            username='profesor1', password='profesor123', role='profesor',
        )
        self.other_profesor = User.objects.create_user(
            username='profesor2', password='profesor123', role='profesor',
        )
        self.course = Course.objects.create(name='1A', academic_year=2026)
        self.other_course = Course.objects.create(name='1B', academic_year=2026)
        TeacherAssignment.objects.create(
            teacher=self.profesor, course=self.course, subject='Matemática',
        )
        self.task = Task.objects.create(
            course=self.course, subject='Matemática',
            title='Tarea 1', description='Desc',
            due_date=date.today() + timedelta(days=7),
            created_by=self.directivo,
        )
        self.list_url = '/api/tasks/'

    def test_list_tasks(self):
        self.client.force_authenticate(user=self.directivo)
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 1)

    def test_filter_by_course(self):
        self.client.force_authenticate(user=self.directivo)
        resp = self.client.get(f'{self.list_url}?course={self.course.id}')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 1)

    def test_filter_by_subject(self):
        self.client.force_authenticate(user=self.directivo)
        resp = self.client.get(f'{self.list_url}?subject=Matemática')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 1)

    def test_filter_by_due_date_range(self):
        self.client.force_authenticate(user=self.directivo)
        today = date.today().isoformat()
        future = (date.today() + timedelta(days=14)).isoformat()
        resp = self.client.get(f'{self.list_url}?due_date_from={today}&due_date_to={future}')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 1)

    def test_search_tasks(self):
        self.client.force_authenticate(user=self.directivo)
        resp = self.client.get(f'{self.list_url}?search=Tarea')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 1)

    def test_teacher_create_task_in_own_course(self):
        self.client.force_authenticate(user=self.profesor)
        data = {
            'course': self.course.id, 'subject': 'Matemática',
            'title': 'Nueva tarea', 'description': 'test',
            'due_date': (date.today() + timedelta(days=3)).isoformat(),
        }
        resp = self.client.post(self.list_url, data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_teacher_create_task_in_other_course_forbidden(self):
        self.client.force_authenticate(user=self.profesor)
        data = {
            'course': self.other_course.id, 'subject': 'Lengua',
            'title': 'Tarea no permitida', 'description': 'test',
            'due_date': (date.today() + timedelta(days=3)).isoformat(),
        }
        resp = self.client.post(self.list_url, data)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_teacher_update_own_course_task(self):
        self.client.force_authenticate(user=self.profesor)
        url = f'{self.list_url}{self.task.id}/'
        resp = self.client.patch(url, {'title': 'Updated Title'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_teacher_delete_other_teacher_task_forbidden(self):
        self.client.force_authenticate(user=self.other_profesor)
        url = f'{self.list_url}{self.task.id}/'
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)


class EventAPITest(APITestCase):
    def setUp(self):
        self.directivo = User.objects.create_user(
            username='directivo', password='admin123', role='directivo',
        )
        self.profesor = User.objects.create_user(
            username='profesor1', password='profesor123', role='profesor',
        )
        self.course = Course.objects.create(name='1A', academic_year=2026)
        TeacherAssignment.objects.create(
            teacher=self.profesor, course=self.course, subject='Matemática',
        )
        self.event = Event.objects.create(
            course=self.course, title='Examen',
            date=date.today() + timedelta(days=10),
            created_by=self.directivo,
        )
        self.list_url = '/api/events/'

    def test_list_events(self):
        self.client.force_authenticate(user=self.directivo)
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 1)

    def test_filter_by_course(self):
        self.client.force_authenticate(user=self.directivo)
        resp = self.client.get(f'{self.list_url}?course={self.course.id}')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 1)

    def test_filter_by_date_range(self):
        self.client.force_authenticate(user=self.directivo)
        today = date.today().isoformat()
        future = (date.today() + timedelta(days=20)).isoformat()
        resp = self.client.get(f'{self.list_url}?date_from={today}&date_to={future}')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 1)

    def test_teacher_create_event_in_own_course(self):
        self.client.force_authenticate(user=self.profesor)
        data = {
            'course': self.course.id, 'title': 'Feriado',
            'date': (date.today() + timedelta(days=5)).isoformat(),
        }
        resp = self.client.post(self.list_url, data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_unauthenticated_blocked(self):
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class GradeAPITest(APITestCase):
    def setUp(self):
        self.directivo = User.objects.create_user(
            username='directivo', password='admin123', role='directivo',
        )
        self.profesor = User.objects.create_user(
            username='profesor1', password='profesor123', role='profesor',
        )
        self.course = Course.objects.create(name='1A', academic_year=2026)
        TeacherAssignment.objects.create(
            teacher=self.profesor, course=self.course, subject='Matemática',
        )
        self.student = Student.objects.create(
            dni='12345678', pin_hash='abc', nombre='Student 1',
            course=self.course,
        )
        self.grade = Grade.objects.create(
            student=self.student, subject='Matemática',
            grade=8.5, period='1er Trimestre',
            created_by=self.directivo,
        )
        self.list_url = '/api/grades/'

    def test_list_grades(self):
        self.client.force_authenticate(user=self.directivo)
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 1)

    def test_filter_by_student(self):
        self.client.force_authenticate(user=self.directivo)
        resp = self.client.get(f'{self.list_url}?student={self.student.id}')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 1)

    def test_filter_by_subject(self):
        self.client.force_authenticate(user=self.directivo)
        resp = self.client.get(f'{self.list_url}?subject=Matemática')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 1)

    def test_filter_by_period(self):
        self.client.force_authenticate(user=self.directivo)
        resp = self.client.get(f'{self.list_url}?period=1er%20Trimestre')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 1)

    def test_teacher_create_grade_in_own_course(self):
        self.client.force_authenticate(user=self.profesor)
        data = {
            'student': self.student.id, 'subject': 'Matemática',
            'grade': 9.0, 'period': '2do Trimestre',
        }
        resp = self.client.post(self.list_url, data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_grade_validation_range(self):
        self.client.force_authenticate(user=self.directivo)
        data = {
            'student': self.student.id, 'subject': 'Matemática',
            'grade': 11, 'period': '1er Trimestre',
        }
        resp = self.client.post(self.list_url, data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
