"""
Seed the database with sample data for development.
Usage:
    DJANGO_SETTINGS_MODULE=config.settings.dev python scripts/seed_sample_data.py
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

import django
django.setup()

from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

User = get_user_model()
from students.models import Student
from academics.models import Course, TeacherAssignment, Schedule, Task, Event


def seed():
    # Users
    admin, _ = User.objects.get_or_create(
        username='directivo',
        defaults={
            'email': 'directivo@colegio.edu',
            'role': User.Role.DIRECTIVO,
            'full_name': 'Directivo Admin',
        }
    )
    admin.set_password('admin123')
    admin.is_staff = True
    admin.is_superuser = True
    admin.save()

    teacher, _ = User.objects.get_or_create(
        username='profesor1',
        defaults={
            'email': 'profesor1@colegio.edu',
            'role': User.Role.PROFESOR,
            'full_name': 'Profesor Uno',
        }
    )
    teacher.set_password('profesor123')
    teacher.save()

    # Courses
    course_1a, _ = Course.objects.get_or_create(name='1A', defaults={'academic_year': 2026})
    course_1b, _ = Course.objects.get_or_create(name='1B', defaults={'academic_year': 2026})

    # Teacher assignments
    TeacherAssignment.objects.get_or_create(teacher=teacher, course=course_1a, subject='Matemáticas')
    TeacherAssignment.objects.get_or_create(teacher=teacher, course=course_1a, subject='Español')

    # Schedules
    for day, start, end, subject in [
        ('Lunes', '08:00', '09:00', 'Matemáticas'),
        ('Lunes', '09:00', '10:00', 'Español'),
        ('Martes', '08:00', '09:00', 'Matemáticas'),
        ('Miércoles', '08:00', '09:00', 'Español'),
    ]:
        Schedule.objects.get_or_create(
            course=course_1a, day=day, start_time=start, end_time=end,
            defaults={'subject': subject, 'teacher': teacher}
        )

    # Student
    student, _ = Student.objects.get_or_create(
        dni='12345678',
        defaults={
            'pin_hash': make_password('4321'),
            'nombre': 'Alumno Prueba',
            'course': course_1a,
        }
    )

    # Tasks
    Task.objects.get_or_create(
        course=course_1a, subject='Matemáticas', title='Resolver ejercicios',
        defaults={'description': 'Páginas 15-20 del libro', 'due_date': '2026-06-01', 'created_by': teacher}
    )

    # Events
    Event.objects.get_or_create(
        course=course_1a, title='Acto del Día de la Bandera',
        defaults={'description': 'Formación en el patio principal', 'date': '2026-06-20', 'created_by': teacher}
    )

    print('Seed data created successfully.')
    print(f'Admin user: directivo / admin123')
    print(f'Teacher:    profesor1 / profesor123')
    print(f'Student:    DNI 12345678 / PIN 4321')


if __name__ == '__main__':
    seed()
