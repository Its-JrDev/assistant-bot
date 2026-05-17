from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Course, TeacherAssignment, Schedule, Task, Event, Grade
from .serializers import (
    CourseSerializer, TeacherAssignmentSerializer, ScheduleSerializer,
    TaskSerializer, EventSerializer, GradeSerializer,
)
from .permissions import IsDirectivoOrReadOnly, IsDirectivoOrTeacherOfCourse


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by('id')
    serializer_class = CourseSerializer
    permission_classes = [IsDirectivoOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ('name',)
    ordering_fields = ('name', 'academic_year')


class TeacherAssignmentViewSet(viewsets.ModelViewSet):
    queryset = TeacherAssignment.objects.select_related('teacher', 'course').all().order_by('id')
    serializer_class = TeacherAssignmentSerializer
    permission_classes = [IsDirectivoOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ('teacher', 'course')
    search_fields = ('subject',)


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.select_related('course', 'teacher').all()
    serializer_class = ScheduleSerializer
    permission_classes = [IsDirectivoOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ('course', 'day')
    ordering_fields = ('course', 'day', 'start_time')


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.select_related('course', 'created_by').all()
    serializer_class = TaskSerializer
    permission_classes = [IsDirectivoOrTeacherOfCourse]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ('course', 'subject')
    search_fields = ('title', 'description')
    ordering_fields = ('due_date', 'created_at')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()
        due_date_from = self.request.query_params.get('due_date_from')
        due_date_to = self.request.query_params.get('due_date_to')
        if due_date_from:
            qs = qs.filter(due_date__gte=due_date_from)
        if due_date_to:
            qs = qs.filter(due_date__lte=due_date_to)
        return qs


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.select_related('course', 'created_by').all()
    serializer_class = EventSerializer
    permission_classes = [IsDirectivoOrTeacherOfCourse]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ('course',)
    search_fields = ('title', 'description')
    ordering_fields = ('date', 'created_at')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        if date_from:
            qs = qs.filter(date__gte=date_from)
        if date_to:
            qs = qs.filter(date__lte=date_to)
        return qs


class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.select_related('student', 'created_by').all()
    serializer_class = GradeSerializer
    permission_classes = [IsDirectivoOrTeacherOfCourse]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ('student', 'subject', 'period')
    ordering_fields = ('student', 'subject', 'period')
