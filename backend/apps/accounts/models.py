from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        DIRECTIVO = 'directivo', 'Directivo'
        PROFESOR = 'profesor', 'Profesor'

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.PROFESOR)
    full_name = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f'{self.get_role_display()}: {self.full_name or self.username}'
