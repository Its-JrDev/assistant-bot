from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from .models import User
from .serializers import UserSerializer, UserDetailSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action == 'list':
            return UserSerializer
        return UserDetailSerializer
