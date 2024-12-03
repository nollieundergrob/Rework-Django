from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    CustomTokenObtainPairView,
    RegisterUserView,
    UserListCreateView,
    AttendanceRecordListCreateView,
    GroupListCreateView,
)

urlpatterns = [
    # Админка
    path('admin/', admin.site.urls),

    # Авторизация
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', RegisterUserView.as_view(), name='register'),

    # Пользователи
    path('users/', UserListCreateView.as_view(), name='user_list_create'),


    # Логи посещаемости
    path('attendance/', AttendanceRecordListCreateView.as_view(), name='attendance_list_create'),

    # Группы
    path('groups/', GroupListCreateView.as_view(), name='group_list_create'),
]
