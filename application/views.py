from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils.timezone import now
from .models import AttendanceRecord, UserModel, Group
from .serializers import AttendanceRecordSerializer, UserSerializer, GroupSerializer,AddUserToGroupSerializer,AggregatedAttendanceSerializer
import logging
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

    def perform_create(self, serializer):
        """Переопределяем создание пользователя для хеширования пароля."""
        user = serializer.save(password=make_password(serializer.validated_data['password']))
        return user

    def post(self, request, *args, **kwargs):
        """Создаёт пользователя и возвращает токен при успешной регистрации."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Сохраняем пользователя
            user = self.perform_create(serializer)

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
                "role": user.role if hasattr(user, 'role') else "undefined",  # Если поле `role` отсутствует
                "telegram_username": user.telegram_username if hasattr(user, 'telegram_username') else None
            }

            # Формируем итоговый ответ
            response_data = {
                "user": user_data,
                "accessToken": access_token,
                "error": False,
                "status": "success"
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        
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

        # Фильтрация по пользователю
        if user_param:
            queryset = queryset.filter(user__username=user_param)

        # Фильтрация по дате
        if date_param:
            try:
                queryset = queryset.filter(timestamp__date=date_param)
            except ValueError:
                # Если дата неверного формата, вернём пустой QuerySet
                queryset = queryset.none()

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

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

        if user_param:
            query_set = query_set.filter(user_username=user_param)
        
        # Фильтрация данных по роли
        if role_param in ['student', 'teacher']:
            query_set = query_set.filter(
                user__role=role_param
            ).select_related('user').prefetch_related('user__student_groups', 'user__teacher_groups')
        # Фильтрация данных
        if date_param:
            try:
                date_filter = pd.to_datetime(date_param).date()
                query_set = query_set.filter(timestamp__date=date_filter).select_related('user').prefetch_related('user__student_groups', 'user__teacher_groups')
            except ValueError:
                return HttpResponse("Invalid date format. Use YYYY-MM-DD.", status=400)
        elif user_param:
            query_set = query_set.filter(user__username=user_param).select_related('user').prefetch_related('user__student_groups', 'user__teacher_groups')
        # Сгруппировать данные по пользователю и дате
        grouped_logs = {}
        for log in query_set:
            user = log.user
            date = log.timestamp.date()
            time_of_entry = log.timestamp.time()

            if (user, date) not in grouped_logs:
                grouped_logs[(user, date)] = {
                    'user': user,
                    'date': date,
                    'morning_entry': None,
                    'afternoon_entry': None
                }

            # Утренний вход
            if time_of_entry < time(12, 30):
                if grouped_logs[(user, date)]['morning_entry'] is None or time_of_entry < grouped_logs[(user, date)]['morning_entry']:
                    grouped_logs[(user, date)]['morning_entry'] = time_of_entry

            # Вход после обеда
            elif time(12, 30) <= time_of_entry:
                if grouped_logs[(user, date)]['afternoon_entry'] is None or time_of_entry < grouped_logs[(user, date)]['afternoon_entry']:
                    grouped_logs[(user, date)]['afternoon_entry'] = time_of_entry

        # Обработать сгруппированные данные
        aggregated_data = []
        for (user, date), logs in grouped_logs.items():
            group_names = ', '.join(list(user.student_groups.values_list('name', flat=True)) + list(user.teacher_groups.values_list('name', flat=True)))

            late_morning = logs['morning_entry'] and not (time(8, 0) <= logs['morning_entry'] <= time(9, 5))
            late_afternoon = logs['afternoon_entry'] and not (time(12, 30) <= logs['afternoon_entry'] <= time(12, 45))
            has_lateness = late_morning or late_afternoon

            aggregated_data.append({
                'username':f'{user.username}',
                'full_name': f"{user.last_name} {user.first_name}",
                'group': group_names,
                'date': date,
                'morning_entry': logs['morning_entry'],
                'afternoon_entry': logs['afternoon_entry'],
                'late_morning': late_morning,
                'late_afternoon': late_afternoon,
                'has_lateness': has_lateness
            })

        # Сериализация данных
        serializer = AggregatedAttendanceSerializer(aggregated_data, many=True)
        return Response(serializer.data)



class AggregatedAttendanceDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Получаем параметры запроса
        query_set = AttendanceRecord.objects.all()
        date_param = request.query_params.get('date', None)
        user_param = request.query_params.get('user', None)
        role_param = request.query_params.get('role', None)

        if user_param:
            query_set = query_set.filter(user_username=user_param)
        
        # Фильтрация данных по роли
        if role_param in ['student', 'teacher']:
            query_set = query_set.filter(
                user__role=role_param
            ).select_related('user').prefetch_related('user__student_groups', 'user__teacher_groups')
        # Фильтрация данных
        if date_param:
            try:
                date_filter = pd.to_datetime(date_param).date()
                query_set = query_set.filter(timestamp__date=date_filter).select_related('user').prefetch_related('user__student_groups', 'user__teacher_groups')
            except ValueError:
                return HttpResponse("Invalid date format. Use YYYY-MM-DD.", status=400)
        elif user_param:
            query_set = query_set.filter(user__username=user_param).select_related('user').prefetch_related('user__student_groups', 'user__teacher_groups')
    
        # Агрегация данных
        data = defaultdict(lambda: {
            'group': None,
            'morning_entry': None,
            'afternoon_entry': None,
            'late_morning': None,
            'late_afternoon': None,
            'has_lateness': None,
        })

        # Сгруппировать данные по пользователю и дате
        grouped_logs = {}
        for log in query_set:
            user = log.user
            date = log.timestamp.date()
            time_of_entry = log.timestamp.time()

            if (user, date) not in grouped_logs:
                grouped_logs[(user, date)] = {
                    'user': user,
                    'date': date,
                    'morning_entry': None,
                    'afternoon_entry': None
                }

            # Утренний вход
            if time_of_entry < time(12, 30):
                if grouped_logs[(user, date)]['morning_entry'] is None or time_of_entry < grouped_logs[(user, date)]['morning_entry']:
                    grouped_logs[(user, date)]['morning_entry'] = time_of_entry

            # Вход после обеда
            elif time(12, 30) <= time_of_entry:
                if grouped_logs[(user, date)]['afternoon_entry'] is None or time_of_entry < grouped_logs[(user, date)]['afternoon_entry']:
                    grouped_logs[(user, date)]['afternoon_entry'] = time_of_entry

        # Обработать сгруппированные данные
        aggregated_data = []
        for (user, date), logs in grouped_logs.items():
            group_names = ', '.join(list(user.student_groups.values_list('name', flat=True)) + list(user.teacher_groups.values_list('name', flat=True)))

            late_morning = logs['morning_entry'] and not (time(8, 0) <= logs['morning_entry'] <= time(9, 5))
            late_afternoon = logs['afternoon_entry'] and not (time(12, 30) <= logs['afternoon_entry'] <= time(12, 45))
            has_lateness = late_morning or late_afternoon

            aggregated_data.append({
                'username':f'{user.username}',
                'full_name': f"{user.last_name} {user.first_name}",
                'group': group_names,
                'date': date,
                'morning_entry': logs['morning_entry'],
                'afternoon_entry': logs['afternoon_entry'],
                'late_morning': late_morning,
                'late_afternoon': late_afternoon,
                'has_lateness': has_lateness
            })

        # Формируем DataFrame
        df = pd.DataFrame(aggregated_data)

        # Указываем правильный порядок столбцов и их заголовки
        df = df[[
            'username',
            'full_name',
            'group',
            'date',
            'morning_entry',
            'afternoon_entry',
            'late_morning',
            'late_afternoon',
            'has_lateness'
        ]]

        # Переименовываем столбцы на понятные
        df.columns = [
            'Username',
            'Фамилия и имя',
            'Группа',
            'Дата',
            'Время утреннего входа',
            'Время обеденного входа',
            'Опоздание утром',
            'Опоздание после обеда',
            'Есть ли опоздания'
        ]

        # Преобразуем булевые значения в читаемые строки
        df['Опоздание утром'] = df['Опоздание утром'].apply(lambda x: 'Опоздал' if x else 'Пришел во время')
        df['Опоздание после обеда'] = df['Опоздание после обеда'].apply(lambda x: 'Опоздал' if x else 'Пришел во время')
        df['Есть ли опоздания'] = df['Есть ли опоздания'].apply(lambda x: 'Есть опоздания' if x else 'Нет опозданий')

        # Создаём файл Excel в памяти
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Attendance')

        # Устанавливаем указатель в начало файла
        output.seek(0)

        # Подготовка ответа для скачивания файла
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="attendance_{now().strftime("%Y%m%d_%H%M%S")}.xlsx"'
        return response

