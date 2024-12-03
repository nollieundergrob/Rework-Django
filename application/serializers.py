from rest_framework import serializers
from datetime import time
from .models import AttendanceRecord, UserModel, Group


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['username', 'password', 'first_name', 'last_name', 'role', 'telegram_username']
        extra_kwargs = {
            'password': {'write_only': True},  # Пароль доступен только для записи
        }

    def create(self, validated_data):
        # Используем метод set_password для хэширования
        user = UserModel(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=validated_data['role'],
            telegram_username=validated_data.get('telegram_username'),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class GroupSerializer(serializers.ModelSerializer):
    teachers = UserSerializer(many=True, read_only=True)
    students = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'teachers', 'students']

class AttendanceRecordSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = AttendanceRecord
        fields = '__all__'
