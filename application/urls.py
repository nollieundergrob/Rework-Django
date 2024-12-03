from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
<<<<<<< HEAD
    CustomTokenObtainPairView,
    RegisterUserView,
    UserListCreateView,
    AttendanceRecordListCreateView,
    GroupListCreateView,
=======
    AttendanceTableView,
    UserModelView,
    GroupView,
    StudentProfileView,
    TeacherProfileView,
    TaskView,
    LoginUser,
    RegisterUser,
>>>>>>> e6f268d1e21adf5848392f8928c09645e3a08976
)

urlpatterns = [
    # Админка
    path('admin/', admin.site.urls),

    # Авторизация
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', RegisterUserView.as_view(), name='register'),

<<<<<<< HEAD
    # Пользователи
    path('users/', UserListCreateView.as_view(), name='user_list_create'),
=======
# Маршруты для студентов
student_patterns = [
    path('api/v1/students/', StudentProfileView.as_view(), name='student-list'),
    path('api/v1/students/<int:pk>/', StudentProfileView.as_view(), name='student-detail'),
]
# Маршруты для учителей
teacher_patterns = [
    path('api/v1/attendance-table/', AttendanceTableView.as_view(), name='attendance-table'),
    path('api/v1/teachers/', TeacherProfileView.as_view(), name='teacher-list'),
    path('api/v1/teachers/<int:pk>/', TeacherProfileView.as_view(), name='teacher-detail'),
]
>>>>>>> e6f268d1e21adf5848392f8928c09645e3a08976


<<<<<<< HEAD
    # Логи посещаемости
    path('attendance/', AttendanceRecordListCreateView.as_view(), name='attendance_list_create'),

    # Группы
    path('groups/', GroupListCreateView.as_view(), name='group_list_create'),
=======
# Марсрушты для вьюшек
view_patterns = [
    path('login/',LoginUser.as_view(),name='login'),
    path('register/',RegisterUser.as_view(), name='register')
    
>>>>>>> e6f268d1e21adf5848392f8928c09645e3a08976
]
