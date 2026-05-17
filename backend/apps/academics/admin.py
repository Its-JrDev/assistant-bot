from django.contrib import admin
from .models import Course, TeacherAssignment, Schedule, Task, Event, Grade


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'academic_year')


@admin.register(TeacherAssignment)
class TeacherAssignmentAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'course', 'subject')
    list_filter = ('course',)


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('course', 'day', 'start_time', 'end_time', 'subject', 'teacher')
    list_filter = ('course', 'day')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'subject', 'due_date')
    list_filter = ('course', 'due_date')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'date')
    list_filter = ('course', 'date')


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'grade', 'period')
    list_filter = ('subject', 'period')
