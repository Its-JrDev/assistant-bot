from rest_framework import permissions


class IsDirectivoOrReadOnly(permissions.BasePermission):
    """Directivos have full access. Others have read-only."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.role == 'directivo'


class IsDirectivoOrTeacherOfCourse(permissions.BasePermission):
    """Directivos have full access. Teachers can only modify their assigned courses."""

    def _get_course_id(self, request, view):
        course_id = request.data.get('course')
        if course_id:
            return course_id
        student_id = request.data.get('student')
        if student_id and view.basename == 'grade':
            from students.models import Student
            try:
                return Student.objects.get(id=student_id).course_id
            except Student.DoesNotExist:
                return None
        return None

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.role == 'directivo':
            return True
        if request.user.role == 'profesor':
            if request.method in permissions.SAFE_METHODS:
                return True
            if request.method == 'POST':
                course_id = self._get_course_id(request, view)
                if course_id:
                    return request.user.assignments.filter(course_id=course_id).exists()
                return False
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'directivo':
            return True
        if request.user.role == 'profesor':
            if request.method in permissions.SAFE_METHODS:
                return True
            course = getattr(obj, 'course', None)
            if course is None and hasattr(obj, 'student'):
                course = obj.student.course
            if course:
                return request.user.assignments.filter(course=course).exists()
            return False
        return False
