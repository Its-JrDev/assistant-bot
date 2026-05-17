from rest_framework import viewsets
from .models import Course, TeacherAssignment, Schedule, Task, Event, Grade
from .serializers import (
    CourseSerializer, TeacherAssignmentSerializer, ScheduleSerializer,
    TaskSerializer, EventSerializer, GradeSerializer,
)
from .permissions import IsDirectivoOrReadOnly, IsDirectivoOrTeacherOfCourse


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsDirectivoOrReadOnly]


class TeacherAssignmentViewSet(viewsets.ModelViewSet):
    queryset = TeacherAssignment.objects.all()
    serializer_class = TeacherAssignmentSerializer
    permission_classes = [IsDirectivoOrReadOnly]


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.select_related('course', 'teacher').all()
    serializer_class = ScheduleSerializer
    permission_classes = [IsDirectivoOrReadOnly]


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.select_related('course', 'created_by').all()
    serializer_class = TaskSerializer
    permission_classes = [IsDirectivoOrTeacherOfCourse]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.select_related('course', 'created_by').all()
    serializer_class = EventSerializer
    permission_classes = [IsDirectivoOrTeacherOfCourse]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.select_related('student', 'created_by').all()
    serializer_class = GradeSerializer
    permission_classes = [IsDirectivoOrTeacherOfCourse]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
