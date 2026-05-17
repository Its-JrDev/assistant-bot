from rest_framework import permissions


class IsDirectivoOrReadOnly(permissions.BasePermission):
    """Directivos have full access. Others have read-only."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.role == 'directivo'


class IsDirectivoOrTeacherOfCourse(permissions.BasePermission):
    """Directivos have full access. Teachers can only modify their assigned courses."""

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'directivo':
            return True
        if request.user.role == 'profesor':
            course = getattr(obj, 'course', None)
            if course:
                return request.user.assignments.filter(course=course).exists()
        return request.method in permissions.SAFE_METHODS
