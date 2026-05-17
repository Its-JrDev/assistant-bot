from django.db import models
from django.conf import settings


class Course(models.Model):
    name = models.CharField(max_length=10, unique=True)
    academic_year = models.IntegerField(default=2026)

    class Meta:
        db_table = 'courses'
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'

    def __str__(self):
        return f'{self.name} ({self.academic_year})'


class TeacherAssignment(models.Model):
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assignments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    subject = models.CharField(max_length=100)

    class Meta:
        db_table = 'teacher_assignments'
        verbose_name = 'Asignación docente'
        verbose_name_plural = 'Asignaciones docentes'
        unique_together = ('teacher', 'course', 'subject')

    def __str__(self):
        return f'{self.teacher.full_name} → {self.course.name} ({self.subject})'


class Schedule(models.Model):
    DAYS = [
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sábado', 'Sábado'),
        ('Domingo', 'Domingo'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='schedules')
    day = models.CharField(max_length=20, choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()
    subject = models.CharField(max_length=100)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    teacher_name = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'schedules'
        verbose_name = 'Horario'
        verbose_name_plural = 'Horarios'
        ordering = ['course', 'day', 'start_time']

    def __str__(self):
        return f'{self.course.name} - {self.day} {self.start_time}-{self.end_time}'


class Task(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='tasks')
    subject = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tasks'
        verbose_name = 'Tarea'
        verbose_name_plural = 'Tareas'
        ordering = ['due_date']

    def __str__(self):
        return f'{self.title} - {self.course.name} ({self.due_date})'


class Event(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=255)
    date = models.DateField()
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'events'
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['date']

    def __str__(self):
        return f'{self.title} - {self.course.name} ({self.date})'


class Grade(models.Model):
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='grades')
    subject = models.CharField(max_length=100)
    grade = models.DecimalField(max_digits=5, decimal_places=2)
    period = models.CharField(max_length=50)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'grades'
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'
        ordering = ['student', 'subject', 'period']

    def __str__(self):
        return f'{self.student.nombre} - {self.subject}: {self.grade}'
