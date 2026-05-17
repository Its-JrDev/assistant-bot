from rest_framework import serializers
from .models import Course, TeacherAssignment, Schedule, Task, Event, Grade


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class TeacherAssignmentSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.full_name', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)

    class Meta:
        model = TeacherAssignment
        fields = '__all__'


class ScheduleSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    teacher_name_display = serializers.CharField(source='teacher.full_name', read_only=True)

    class Meta:
        model = Schedule
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('created_at',)


class EventSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ('created_at',)


class GradeSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.nombre', read_only=True)
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)

    class Meta:
        model = Grade
        fields = '__all__'
        read_only_fields = ('created_at',)
