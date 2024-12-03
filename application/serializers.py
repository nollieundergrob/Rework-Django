from datetime import date, time
from rest_framework import serializers
<<<<<<< HEAD
from datetime import time
from .models import AttendanceRecord, UserModel, Group

=======
from .models import UserModel, Group, StudentProfile, TeacherProfile, Attendance, Task, TaskSubmission, TaskRating
from django.db.models import Q, F, Min, Case, When, Value, DateTimeField, TimeField
>>>>>>> e6f268d1e21adf5848392f8928c09645e3a08976

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

<<<<<<< HEAD
class AttendanceRecordSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = AttendanceRecord
        fields = '__all__'
=======

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class TaskSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskSubmission
        fields = '__all__'


class TaskRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskRating
        fields = '__all__'


from rest_framework import serializers
from .models import Attendance, StudentProfile
from datetime import time
from django.db.models import Min, Max
from rest_framework import serializers

class AggregatedAttendanceTableSerializer(serializers.Serializer):
    fio = serializers.CharField()
    date = serializers.DateField()
    group = serializers.CharField()
    morning_time = serializers.TimeField(allow_null=True)
    after_lunch_time = serializers.TimeField(allow_null=True)
    lateness = serializers.CharField()

    @classmethod
    def get_aggregated_data(cls, queryset):
        # Группировка данных по студенту и дате
        aggregated_data = queryset.values(
            'student', 
            'student__user__user_full_name', 
            'student__group__name'
        ).annotate(
            first_morning_time=Min(  # Первое вхождение утром до 9:00
                Case(
                    When(
                        timestamp__time__lt=time(9, 0),
                        then=F('timestamp__time')
                    ),
                    default=None,
                    output_field=TimeField()
                )
            ),
            first_after_lunch_time=Min(  # Первое вхождение после 12:40
                Case(
                    When(
                        timestamp__time__gte=time(12, 40),
                        then=F('timestamp__time')
                    ),
                    default=None,
                    output_field=TimeField()
                )
            )
        )


        # Преобразуем данные для сериализации
        results = []
        for record in aggregated_data:
            lateness = "+"
            if record['first_morning_time'] and record['first_morning_time'] <= time(9, 0):
                lateness = ""
            results.append({
                'fio': record['student__user__user_full_name'],
                'date': queryset.first().timestamp.date(),  # Берем дату из queryset
                'group': record['student__group__name'],
                'morning_time': record['first_morning_time'],
                'after_lunch_time': record['first_after_lunch_time'],
                'lateness': lateness,
            })
        return results
>>>>>>> e6f268d1e21adf5848392f8928c09645e3a08976
