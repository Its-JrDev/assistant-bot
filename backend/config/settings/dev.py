from .base import *
import os

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-dev-key-not-for-production')
DEBUG = True
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.dev.sqlite3',
    }
}

CORS_ALLOW_ALL_ORIGINS = True
