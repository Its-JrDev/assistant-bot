from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.views import UserViewSet
from students.views import StudentViewSet
from academics.views import (
    CourseViewSet, TeacherAssignmentViewSet, ScheduleViewSet,
    TaskViewSet, EventViewSet, GradeViewSet,
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'students', StudentViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'assignments', TeacherAssignmentViewSet)
router.register(r'schedules', ScheduleViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'events', EventViewSet)
router.register(r'grades', GradeViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
