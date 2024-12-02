from django.urls import path
from .views import (
    UserModelView,
    GroupView,
    StudentProfileView,
    TeacherProfileView,
    TaskView,
    LoginUser,
    RegisterUser,
)

# utils_pattern = [
#     path('attendance/', utils.AttendanceReportGenerator.generate_report,)
# ]
# Маршруты для пользователей
user_patterns = [
    path('api/v1/users/', UserModelView.as_view(), name='user-list'),
    path('api/v1/users/<int:pk>/', UserModelView.as_view(), name='user-detail'),
]

# Маршруты для групп
group_patterns = [
    path('api/v1/groups/', GroupView.as_view(), name='group-list'),
    path('api/v1/groups/<int:pk>/', GroupView.as_view(), name='group-detail'),
]

# Маршруты для студентов
student_patterns = [
    path('api/v1/students/', StudentProfileView.as_view(), name='student-list'),
    path('api/v1/students/<int:pk>/', StudentProfileView.as_view(), name='student-detail'),
]
# Маршруты для учителей
teacher_patterns = [
    path('api/v1/teachers/', TeacherProfileView.as_view(), name='teacher-list'),
    path('api/v1/teachers/<int:pk>/', TeacherProfileView.as_view(), name='teacher-detail'),
]

# Маршруты для заданий
task_patterns = [
    path('api/v1/tasks/', TaskView.as_view(), name='task-list'),
    path('api/v1/tasks/<int:pk>/', TaskView.as_view(), name='task-detail'),
]

# Марсрушты для вьюшек
view_patterns = [
    path('login/',LoginUser.as_view(),name='login'),
    path('register/',RegisterUser.as_view(), name='register')
]
# Финальный список маршрутов
urlpatterns = view_patterns+ user_patterns + group_patterns + student_patterns + teacher_patterns + task_patterns  
