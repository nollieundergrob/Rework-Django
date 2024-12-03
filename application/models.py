from django.contrib.auth.models import AbstractUser, Group as AuthGroup, Permission as AuthPermission
from django.db import models

from django.contrib.auth.models import AbstractUser, Group as AuthGroup, Permission as AuthPermission
from django.db import models

class UserModel(AbstractUser):
    """
    Кастомная модель пользователя.
    """
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    telegram_username = models.CharField(max_length=64, blank=True, null=True)

    groups = models.ManyToManyField(
        AuthGroup,
        related_name="custom_user_groups",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups"
    )
    user_permissions = models.ManyToManyField(
        AuthPermission,
        related_name="custom_user_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions"
    )

    def __str__(self):
        return f"{self.username} ({self.role})"


class Group(models.Model):
    name = models.CharField(max_length=128, unique=True)
    teachers = models.ManyToManyField(
        UserModel,
        limit_choices_to={'role': 'teacher'},
        related_name='teacher_groups',
        blank=True
    )
    students = models.ManyToManyField(
        UserModel,
        limit_choices_to={'role': 'student'},
        related_name='student_groups',
        blank=True
    )

    def __str__(self):
        return self.name

<<<<<<< HEAD
class AttendanceRecord(models.Model):
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    request_method = models.CharField(max_length=10, null=True, blank=True)
    request_url = models.URLField(null=True, blank=True)
    headers = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.timestamp}"
=======

class StudentProfile(models.Model):
    """
    Профиль студента
    """
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='student_profile')
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, related_name='students')

    def __str__(self):
        return f'{self.user.user_full_name} - {self.group}'


class TeacherProfile(models.Model):
    """
    Профиль учителя
    """
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='teacher_profile')
    rank = models.CharField(max_length=64)

    def __str__(self):
        return self.user.user_full_name


class Attendance(models.Model):
    """
    Посещения студентов
    """
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='attendance')
    ip_address = models.GenericIPAddressField()
    user_agent = models.JSONField()  # Хранить данные user-agent
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f'{self.student} - {self.timestamp}'


class Task(models.Model):
    """
    Задания
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    hash_value = models.CharField(max_length=65, unique=True)
    status = models.BooleanField(default=True)
    max_rate = models.PositiveIntegerField()

    def __str__(self):
        return self.title


class TaskSubmission(models.Model):
    """
    Ответы на задания
    """
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='submissions')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='submissions')
    file = models.FileField(upload_to='media/task/files')
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f'{self.student} - {self.task}'


class TaskRating(models.Model):
    """
    Оценка задания
    """
    answer = models.ForeignKey(TaskSubmission, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.answer} - {self.rating}'
>>>>>>> e6f268d1e21adf5848392f8928c09645e3a08976
