from datetime import date, time
from rest_framework import serializers
from .models import UserModel, Group, StudentProfile, TeacherProfile, Attendance, Task, TaskSubmission, TaskRating
from django.db.models import Q, F, Min, Case, When, Value, DateTimeField, TimeField

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserModelSerializer()

    class Meta:
        model = StudentProfile
        fields = '__all__'


class TeacherProfileSerializer(serializers.ModelSerializer):
    user = UserModelSerializer()

    class Meta:
        model = TeacherProfile
        fields = '__all__'


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'


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