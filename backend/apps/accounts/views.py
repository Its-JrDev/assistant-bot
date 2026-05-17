from rest_framework import viewsets
from rest_framework.permissions import BasePermission
from .models import User
from .serializers import UserSerializer, UserDetailSerializer


class IsDirectivo(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'directivo'


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    permission_classes = [IsDirectivo]

    def get_serializer_class(self):
        if self.action == 'list':
            return UserSerializer
        return UserDetailSerializer
