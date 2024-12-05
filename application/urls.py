from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    AttachFileToAttendanceView,
    CustomTokenObtainPairView,
    RegisterUserView,
    UserListCreateUpdateView,
    AttendanceRecordListCreateView,
    GroupListCreateView,
    AddUserToGroupView,
    AggregatedAttendanceView,
    AggregatedAttendanceDownloadView,
)

urlpatterns = [ 

    # Авторизация
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('auth/register/', RegisterUserView.as_view(), name='register'),

    # Пользователи
    path('data/', UserListCreateUpdateView.as_view(), name='user_list_create'),
    path('data/<int:pk>/', UserListCreateUpdateView.as_view(), name='user_update'),

    # Логи посещаемости
    path('attendance/aggregated/download/', AggregatedAttendanceDownloadView.as_view(), name='aggregated_attendance'),
    path('attendance/aggregated/', AggregatedAttendanceView.as_view(), name='aggregated_attendance'),
    path('attendance/', AttendanceRecordListCreateView.as_view(), name='attendance_list_create'),
    path('attendance/attach_file/', AttachFileToAttendanceView.as_view(), name='attach_file_to_attendance'),

    # Группы
    path('groups/', GroupListCreateView.as_view(), name='group_list_create'),
    path('groups/<int:group_id>/add_user/', AddUserToGroupView.as_view(), name='add_user_to_group'),
]

