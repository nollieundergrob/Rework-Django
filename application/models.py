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
    @property
    def has_files(self):
        return self.attendancefile_set.exists()

class AttendanceFile(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='attendance_files')
    date = models.DateField()  # Привязка файла к дате
    file = models.FileField(upload_to='attendance/files')  # Загружаемый файл

    def __str__(self):
        return f"File for {self.user.username} on {self.date}: {self.file.name}"