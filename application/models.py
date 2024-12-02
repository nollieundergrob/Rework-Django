from django.db import models
from django.utils.timezone import now


class UserModel(models.Model):
    """
    Модель пользователя
    """
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]
    user_full_name = models.CharField('ФИО', max_length=100)
    user_login = models.CharField('Username', max_length=100, unique=True)
    user_hash_value = models.CharField(db_index=True, max_length=65)
    user_password = models.CharField(max_length=128)  # Лучше использовать хэшированный пароль
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    telegram_username = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return f'{self.user_full_name} ({self.role})'


class Group(models.Model):
    """
    Модель группы студентов
    """
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


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


class AttendanceRecord(models.Model):
    student = models.ForeignKey('StudentProfile', on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    morning_status = models.CharField(max_length=50, null=True, blank=True)
    lunch_status = models.CharField(max_length=50, null=True, blank=True)
    morning_time = models.TimeField(null=True, blank=True)
    lunch_time = models.TimeField(null=True, blank=True)
    lateness = models.CharField(max_length=5, default='', blank=True)

    def __str__(self):
        return f'{self.student} - {self.date}'
