from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

User = get_user_model()
from students.models import Student
from academics.models import Course, TeacherAssignment, Schedule, Task, Event


class Command(BaseCommand):
    help = 'Seed sample data for development'

    def handle(self, *args, **options):
        if User.objects.filter(username='directivo').exists():
            self.stdout.write('Seed data already exists, skipping.')
            return

        admin = User.objects.create_superuser(
            username='directivo', password='admin123',
            email='directivo@colegio.edu', role=User.Role.DIRECTIVO,
            full_name='Directivo Admin', is_staff=True,
        )
        teacher = User.objects.create_user(
            username='profesor1', password='profesor123',
            email='profesor1@colegio.edu', role=User.Role.PROFESOR,
            full_name='Profesor Uno',
        )
        course_1a = Course.objects.create(name='1A', academic_year=2026)
        Course.objects.create(name='1B', academic_year=2026)

        TeacherAssignment.objects.create(teacher=teacher, course=course_1a, subject='Matemáticas')
        TeacherAssignment.objects.create(teacher=teacher, course=course_1a, subject='Español')

        for day, start, end, subject in [
            ('Lunes', '08:00', '09:00', 'Matemáticas'),
            ('Lunes', '09:00', '10:00', 'Español'),
            ('Martes', '08:00', '09:00', 'Matemáticas'),
            ('Miércoles', '08:00', '09:00', 'Español'),
        ]:
            Schedule.objects.create(
                course=course_1a, day=day, start_time=start, end_time=end,
                subject=subject, teacher=teacher,
            )

        Student.objects.create(
            dni='12345678', pin_hash=make_password('4321'),
            nombre='Alumno Prueba', course=course_1a,
        )
        Task.objects.create(
            course=course_1a, subject='Matemáticas', title='Resolver ejercicios',
            description='Páginas 15-20 del libro', due_date='2026-06-01', created_by=teacher,
        )
        Event.objects.create(
            course=course_1a, title='Acto del Día de la Bandera',
            description='Formación en el patio principal', date='2026-06-20', created_by=teacher,
        )

        self.stdout.write('Seed data created successfully.')
