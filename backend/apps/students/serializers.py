from rest_framework import serializers
from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'dni', 'nombre', 'course', 'telegram_id')
        read_only_fields = ('id',)
