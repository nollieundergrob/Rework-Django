from datetime import date, time
from rest_framework import serializers
from datetime import time
from .models import AttendanceFile, AttendanceRecord, UserModel, Group


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['username', 'password', 'first_name', 'last_name', 'role', 'telegram_username']
        extra_kwargs = {
            'password': {'write_only': True},  # Пароль доступен только для записи
        }

    def create(self, validated_data):
        # Создание нового пользователя с хэшированием пароля
        if 'role' not in validated_data:
            validated_data['role'] == 'student'
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

    def update(self, instance, validated_data):
        # Обновление существующего пользователя
        for attr, value in validated_data.items():
            if attr == 'password':
                # Хэшируем пароль перед сохранением
                instance.set_password(value)
            else:
                # Обновляем другие поля
                setattr(instance, attr, value)
        instance.save()
        return instance


class GroupSerializer(serializers.ModelSerializer):
    teachers = UserSerializer(many=True, read_only=True)
    students = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'teachers', 'students']



class AddUserToGroupSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    role = serializers.ChoiceField(choices=['teacher', 'student'])

    def validate(self, data):
        user_id = data.get('user_id')
        role = data.get('role')

        # Проверяем, существует ли пользователь с таким ID
        try:
            user = UserModel.objects.get(id=user_id)
        except UserModel.DoesNotExist:
            raise serializers.ValidationError("Пользователь с таким ID не найден.")

        # Проверяем роль пользователя
        if user.role != role:
            raise serializers.ValidationError(f"Пользователь с ID {user_id} не является {role}.")
        return data

class AggregatedAttendanceSerializer(serializers.Serializer):
    id =serializers.IntegerField()
    username = serializers.CharField()
    full_name = serializers.CharField()
    date = serializers.DateField(format='%d.%m.%Y')
    morning_entry = serializers.TimeField(allow_null=True)
    afternoon_entry = serializers.TimeField(allow_null=True)
    late_morning = serializers.BooleanField()
    late_afternoon = serializers.BooleanField()
    has_lateness = serializers.BooleanField()
    files = serializers.ListField()
    

class AttendanceFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceFile
        fields = ['id','record', 'file']


class AttendanceRecordSerializer(serializers.ModelSerializer):
    files = AttendanceFileSerializer(many=True, read_only=True)
    file_upload = serializers.FileField(write_only=True, required=False)

    class Meta:
        model = AttendanceRecord
        fields = ['id', 'user', 'timestamp', 'files', 'file_upload']

    def create(self, validated_data):
        file_data = validated_data.pop('file_upload', None)
        attendance_record = super().create(validated_data)

        if file_data:
            AttendanceFile.objects.create(record=attendance_record, file=file_data)

        return attendance_record