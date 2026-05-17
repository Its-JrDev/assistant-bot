"""
Migrate data from legacy SQLite to Django ORM.
Run after models are created and migrations are applied.

Usage:
    DJANGO_SETTINGS_MODULE=config.settings.dev python scripts/migrate_sqlite_to_django.py
"""
import os
import sys
from pathlib import Path

# Setup Django
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

import django
django.setup()

import sqlite3
from django.contrib.auth.hashers import make_password

# Legacy SQLite path
LEGACY_DB = Path(__file__).parent.parent / 'database' / 'data.db'

# Import Django models after setup
from django.contrib.auth import get_user_model
from students.models import Student
from academics.models import Course, Schedule, Task, Event


def get_legacy_connection():
    if not LEGACY_DB.exists():
        print(f'Legacy database not found at {LEGACY_DB}')
        return None
    return sqlite3.connect(str(LEGACY_DB))


def migrate_courses(conn):
    """Extract unique courses from legacy data."""
    cur = conn.cursor()
    cur.execute('SELECT DISTINCT curso FROM horarios')
    courses = []
    for (name,) in cur.fetchall():
        course, _ = Course.objects.get_or_create(name=name, defaults={'academic_year': 2026})
        courses.append(name)
    print(f'  ✓ {len(courses)} courses migrated')
    return courses


def migrate_students(conn):
    cur = conn.cursor()
    cur.execute('SELECT id, dni, pin, nombre, curso, telegram_id, logged FROM estudiantes')
    count = 0
    for row in cur.fetchall():
        course = Course.objects.filter(name=row[4]).first()
        Student.objects.update_or_create(
            dni=row[1],
            defaults={
                'pin_hash': make_password(row[2]),
                'nombre': row[3],
                'course': course,
                'telegram_id': row[5],
                'is_logged': bool(row[6]),
            }
        )
        count += 1
    print(f'  ✓ {count} students migrated (PINs hashed)')


def migrate_schedules(conn):
    cur = conn.cursor()
    cur.execute('SELECT curso, dia, hora_inicio, hora_fin, asignatura, profesor FROM horarios')
    count = 0
    for row in cur.fetchall():
        course = Course.objects.filter(name=row[0]).first()
        if not course:
            continue
        Schedule.objects.create(
            course=course,
            day=row[1],
            start_time=row[2],
            end_time=row[3],
            subject=row[4],
            teacher_name=row[5],
        )
        count += 1
    print(f'  ✓ {count} schedules migrated')


def migrate_tasks(conn):
    cur = conn.cursor()
    cur.execute('SELECT curso, materia, titulo, descripcion, fecha_entrega FROM tareas')
    count = 0
    for row in cur.fetchall():
        course = Course.objects.filter(name=row[0]).first()
        if not course:
            continue
        Task.objects.create(
            course=course,
            subject=row[1],
            title=row[2],
            description=row[3],
            due_date=row[4],
        )
        count += 1
    print(f'  ✓ {count} tasks migrated')


def migrate_events(conn):
    cur = conn.cursor()
    cur.execute('SELECT curso, evento, fecha, descripcion FROM eventos')
    count = 0
    for row in cur.fetchall():
        course = Course.objects.filter(name=row[0]).first()
        if not course:
            continue
        Event.objects.create(
            course=course,
            title=row[1],
            date=row[2],
            description=row[3],
        )
        count += 1
    print(f'  ✓ {count} events migrated')


def main():
    conn = get_legacy_connection()
    if not conn:
        print('No legacy database found. Skipping migration.')
        return

    print('Migrating from legacy SQLite to Django ORM...')
    migrate_courses(conn)
    migrate_students(conn)
    migrate_schedules(conn)
    migrate_tasks(conn)
    migrate_events(conn)
    conn.close()
    print('Migration complete.')


if __name__ == '__main__':
    main()
