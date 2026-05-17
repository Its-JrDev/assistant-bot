from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'dni', 'course', 'telegram_id')
    list_filter = ('course',)
    search_fields = ('nombre', 'dni')
