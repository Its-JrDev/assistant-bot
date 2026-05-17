from django.db import models


class Student(models.Model):
    dni = models.CharField(max_length=11, unique=True)
    pin_hash = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255)
    course = models.ForeignKey('academics.Course', on_delete=models.SET_NULL, null=True, blank=True)
    telegram_id = models.BigIntegerField(unique=True, null=True, blank=True)

    class Meta:
        db_table = 'students'
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'

    def __str__(self):
        return f'{self.nombre} ({self.dni})'
