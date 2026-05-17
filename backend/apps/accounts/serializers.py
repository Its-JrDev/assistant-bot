from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'full_name', 'is_active')
        read_only_fields = ('id',)


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'full_name', 'is_active', 'date_joined')
        read_only_fields = ('id', 'date_joined')
