from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils.timezone import now
from .models import AttendanceFile, AttendanceRecord, UserModel, Group
from .serializers import AttendanceFileSerializer, AttendanceRecordSerializer, UserSerializer, GroupSerializer,AddUserToGroupSerializer,AggregatedAttendanceSerializer
import logging
from django.db import models
from django.utils.timezone import localtime
from collections import defaultdict
from datetime import time 
import pandas as pd
from django.http import HttpResponse
from io import BytesIO

logger = logging.getLogger('django')

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        # Проверяем успешную авторизацию
        if response.status_code == 200:
            username = request.data.get('username')
            try:
                user = UserModel.objects.get(username=username)
                # Регистрируем посещаемость вручную
                AttendanceRecord.objects.create(
                    user=user,
                    timestamp=now(),
                    ip_address=request.META.get('REMOTE_ADDR', 'Unknown'),
                    user_agent=request.META.get('HTTP_USER_AGENT', 'Unknown'),
                    request_method=request.method,
                    request_url=request.build_absolute_uri(),
                    headers={k: v for k, v in request.headers.items()},
                )
                logger.info(f"Attendance logged for user {user.username}")
            except UserModel.DoesNotExist:
                logger.error(f"User {username} not found for attendance logging")
        print(response)
        return response

from rest_framework import generics, mixins
from rest_framework.permissions import AllowAny
from .models import UserModel
from .serializers import UserSerializer

from django.contrib.auth.hashers import make_password

from rest_framework import generics, mixins, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.timezone import now
from .models import UserModel, AttendanceRecord
from .serializers import UserSerializer
from django.contrib.auth.hashers import make_password
import logging

logger = logging.getLogger(__name__)

class UserListCreateUpdateView(generics.ListCreateAPIView, mixins.UpdateModelMixin):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


    def post(self, request, *args, **kwargs):
        """Создаёт пользователя и возвращает токен при успешной регистрации."""
        if 'role' not in request.data:
            request.data['role'] = 'student'
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                # Сохраняем пользователя
                user = serializer.save()

                if user is None:
                    raise ValueError("Failed to create user")

                # Генерируем токены для зарегистрированного пользователя
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                # Логируем посещение
                AttendanceRecord.objects.create(
                    user=user,
                    timestamp=now(),
                    ip_address=request.META.get('REMOTE_ADDR', 'Unknown'),
                    user_agent=request.META.get('HTTP_USER_AGENT', 'Unknown'),
                    request_method=request.method,
                    request_url=request.build_absolute_uri(),
                )

                logger.info(f"User {user.username} registered and attendance logged")

                # Формируем пользовательскую часть ответа
                user_data = {
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": user.role if hasattr(user, 'role') else "undefined",
                    "telegram_username": user.telegram_username if hasattr(user, 'telegram_username') else None,
                }

                # Формируем итоговый ответ
                response_data = {
                    "user": user_data,
                    "accessToken": access_token,
                    "error": False,
                    "status": "success",
                }

                return Response(response_data, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error(f"Error during user creation: {str(e)}")
                return Response(
                    {
                        "error": True,
                        "status": "failed",
                        "message": f"User creation failed due to server error. {str(e)} "
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        # Если данные некорректны, возвращаем ошибку
        return Response(
            {
                "error": True,
                "status": "failed",
                "message": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

        
        # Если данные некорректны, возвращаем ошибку
        return Response(
            {
                "error": True,
                "status": "failed",
                "message": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    def put(self, request, *args, **kwargs):
        """Обновление пользователя."""
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """Частичное обновление пользователя."""
        return self.partial_update(request, *args, **kwargs)


class AttendanceRecordListCreateView(generics.ListCreateAPIView):
    serializer_class = AttendanceRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = AttendanceRecord.objects.all().order_by('-timestamp')
        user_param = self.request.query_params.get('user', None)
        date_param = self.request.query_params.get('date', None)
        has_files = self.request.query_params.get('has_files', None)

        # Фильтрация по пользователю
        if user_param:
            queryset = queryset.filter(user__username=user_param)

        # Фильтрация по дате
        if date_param:
            queryset = queryset.filter(timestamp__date=date_param)

        # Фильтрация по наличию файлов
        if has_files is not None:
            if has_files.lower() == 'true':
                file_users_dates = AttendanceFile.objects.values_list('user', 'date')
                queryset = queryset.filter(
                    user__in=[item[0] for item in file_users_dates],
                    timestamp__date__in=[item[1] for item in file_users_dates]
                )
            elif has_files.lower() == 'false':
                file_users_dates = AttendanceFile.objects.values_list('user', 'date')
                queryset = queryset.exclude(
                    user__in=[item[0] for item in file_users_dates],
                    timestamp__date__in=[item[1] for item in file_users_dates]
                )

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AttachFileToAttendanceView(APIView):
    """
    Эндпоинт для добавления файла, связанного с пользователем и датой.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.data.get('user_id')
        date = request.data.get('date')
        file = request.FILES.get('file')

        # Проверяем наличие всех необходимых данных
        if not user_id or not date or not file:
            return Response(
                {"error": "Пожалуйста, предоставьте user_id, дату (в формате YYYY-MM-DD) и файл."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Проверяем существование пользователя
        try:
            user = UserModel.objects.get(id=user_id)
        except UserModel.DoesNotExist:
            return Response({"error": "Пользователь не найден."}, status=status.HTTP_404_NOT_FOUND)

        # Проверяем корректность формата даты
        try:
            date_obj = pd.to_datetime(date).date()
        except ValueError:
            return Response({"error": "Некорректный формат даты. Используйте YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        # Создаем файл
        try:
            attendance_file = AttendanceFile.objects.create(user=user, date=date_obj, file=file)
        except Exception as e:
            return Response({"error": f"Ошибка при добавлении файла: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Сериализация и ответ
        serializer = AttendanceFileSerializer(attendance_file)
        return Response(serializer.data, status=status.HTTP_201_CREATED)




class GroupListCreateView(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

from rest_framework import generics
from .models import UserModel
from .serializers import UserSerializer

class RegisterUserView(generics.CreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Открываем доступ для всех



class AddUserToGroupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, group_id):
        # Проверка данных
        serializer = AddUserToGroupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data['user_id']
        role = serializer.validated_data['role']

        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return Response({"error": "Группа не найдена."}, status=status.HTTP_404_NOT_FOUND)

        user = UserModel.objects.get(id=user_id)

        # Добавление пользователя в группу
        if role == 'teacher':
            group.teachers.add(user)
        elif role == 'student':
            group.students.add(user)

        return Response({"message": f"Пользователь {user.username} добавлен в группу {group.name} как {role}."},
                        status=status.HTTP_200_OK)



class AggregatedAttendanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        query_set = AttendanceRecord.objects.all()
        date_param = request.query_params.get('date', None)
        user_param = request.query_params.get('user', None)
        role_param = request.query_params.get('role', None)

        # Фильтрация по параметрам
        if user_param:
            query_set = query_set.filter(user__username=user_param)

        if role_param in ['student', 'teacher']:
            query_set = query_set.filter(user__role=role_param)

        if date_param:
            query_set = query_set.filter(timestamp__date=date_param)

        # Группировка данных
        grouped_logs = {}
        for log in query_set:
            user = log.user
            date = log.timestamp.date()
            time_of_entry = log.timestamp.time()

            # Получаем файлы для текущей даты и пользователя
            files_queryset = AttendanceFile.objects.filter(user=user, date=date)
            files = ['http://' + request.get_host() + f.file.url for f in files_queryset]

            if (user, date) not in grouped_logs:
                grouped_logs[(user, date)] = {
                    'user': user,
                    'date': date,
                    'morning_entry': None,
                    'afternoon_entry': None,
                    'files': files
                }

            # Определяем самое раннее и позднее время входа
            if time_of_entry < time(12, 30):
                if grouped_logs[(user, date)]['morning_entry'] is None or time_of_entry < grouped_logs[(user, date)]['morning_entry']:
                    grouped_logs[(user, date)]['morning_entry'] = time_of_entry
            else:
                if grouped_logs[(user, date)]['afternoon_entry'] is None or time_of_entry < grouped_logs[(user, date)]['afternoon_entry']:
                    grouped_logs[(user, date)]['afternoon_entry'] = time_of_entry

        # Формирование ответа
        aggregated_data = []
        for (user, date), logs in grouped_logs.items():
            group_names = ', '.join(list(user.student_groups.values_list('name', flat=True)) + list(user.teacher_groups.values_list('name', flat=True)))
            aggregated_data.append({
                'id': user.id,
                'username': user.username,
                'full_name': f"{user.last_name} {user.first_name}",
                'group': group_names,
                'date': date,
                'morning_entry': logs['morning_entry'],
                'afternoon_entry': logs['afternoon_entry'],
                'files': logs['files']
            })

        return Response(aggregated_data)




class AggregatedAttendanceDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        query_set = AttendanceRecord.objects.all()
        date_param = request.query_params.get('date', None)

        if date_param:
            query_set = query_set.filter(timestamp__date=date_param)

        # Агрегация данных
        grouped_data = {}
        for log in query_set:
            user = log.user
            date = log.timestamp.date()

            # Получаем файлы для текущего пользователя и даты
            files_queryset = AttendanceFile.objects.filter(user=user, date=date)
            files = ['http://' + request.get_host() + f.file.url for f in files_queryset]

            if (user.id, date) not in grouped_data:
                grouped_data[(user.id, date)] = {
                    'id': user.id,
                    'username': user.username,
                    'full_name': f"{user.last_name} {user.first_name}",
                    'date': date,
                    'morning_entry': None,
                    'afternoon_entry': None,
                    'files': files
                }

        # Создание DataFrame
        aggregated_data = list(grouped_data.values())
        df = pd.DataFrame(aggregated_data)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Attendance')

        output.seek(0)
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="attendance_{now().strftime("%Y%m%d_%H%M%S")}.xlsx"'
        return response
