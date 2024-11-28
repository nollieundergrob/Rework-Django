from rest_framework import serializers
from .models import UserModel, Group, StudentProfile, TeacherProfile, Attendance, Task, TaskSubmission, TaskRating


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
