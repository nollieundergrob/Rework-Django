from django.urls import path
from .views import (
    UserModelView,
    GroupView,
    StudentProfileView,
    TeacherProfileView,
    TaskView,
)

# Маршруты для пользователей
user_patterns = [
    path('users/', UserModelView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserModelView.as_view(), name='user-detail'),
]

# Маршруты для групп
group_patterns = [
    path('groups/', GroupView.as_view(), name='group-list'),
    path('groups/<int:pk>/', GroupView.as_view(), name='group-detail'),
]

# Маршруты для студентов
student_patterns = [
    path('students/', StudentProfileView.as_view(), name='student-list'),
    path('students/<int:pk>/', StudentProfileView.as_view(), name='student-detail'),
]

# Маршруты для учителей
teacher_patterns = [
    path('teachers/', TeacherProfileView.as_view(), name='teacher-list'),
    path('teachers/<int:pk>/', TeacherProfileView.as_view(), name='teacher-detail'),
]

# Маршруты для заданий
task_patterns = [
    path('tasks/', TaskView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskView.as_view(), name='task-detail'),
]

# Финальный список маршрутов
urlpatterns = user_patterns + group_patterns + student_patterns + teacher_patterns + task_patterns
