<<<<<<< HEAD
from rest_framework import generics, status
=======
import json
from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from .models import Attendance, UserModel, Group, StudentProfile, TeacherProfile, Task
from .serializers import (
    AggregatedAttendanceTableSerializer,
    AttendanceSerializer,
    UserModelSerializer,
    GroupSerializer,
    StudentProfileSerializer,
    TeacherProfileSerializer,
    TaskSerializer,
    
)
from django.utils.dateparse import parse_date
from . import utils
from django.http import *
from hashlib import sha256
>>>>>>> e6f268d1e21adf5848392f8928c09645e3a08976
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils.timezone import now
from .models import AttendanceRecord, UserModel, Group
from .serializers import AttendanceRecordSerializer, UserSerializer, GroupSerializer
import logging

logger = logging.getLogger('django')

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            logger.info(f"Successful login for user {response.data.get('username')}")
        else:
            logger.error(f"Failed login attempt: {response.data}")
        return response

class UserListCreateView(generics.ListCreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class AttendanceRecordListCreateView(generics.ListCreateAPIView):
    queryset = AttendanceRecord.objects.all().order_by('-timestamp')
    serializer_class = AttendanceRecordSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class GroupListCreateView(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

<<<<<<< HEAD
from rest_framework import generics
from .models import UserModel
from .serializers import UserSerializer
=======
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# CRUD для профилей студентов
class StudentProfileView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# CRUD для профилей учителей
class TeacherProfileView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherProfileSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# CRUD для заданий
class TaskView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class LoginUser(APIView):
    salt = 'anfkgzp2201!_asd0Fo__:::SECURITY_HASH_SALTING:0xAFFCBA'
    def get(self,request):
        return render(request,'login.html')
    
    def post(self, request):
        login = request.data.get('login')
        password = request.data.get('password')

        if not login or not password:
            return Response({'error': 'Login and password are required'}, status=400)

        password += self.salt
        hashed_password = sha256(password.encode('utf-8')).hexdigest()
        hash_account = sha256(f'{login}DPAD!_saltjoJoad{password}'.encode('utf-8')).hexdigest()

        user = UserModel.objects.filter(user_hash_value=hash_account).first()
        if not user:
            return Response({'error': 'User not found'}, status=404)

        # Генерация JWT токенов
        refresh = RefreshToken.for_user(user)

        # Логирование посещения
        ip_address = utils.get_root_ip(request)
        user_agent = request.headers.get('User-Agent', '')
        if user.role == 'student':
            attendance_data = {
                'student': user.id,
                'ip_address': ip_address,
                'user_agent': json.dumps({'user_agent': user_agent}),
                'timestamp': datetime.datetime.now(),
            }
            attendance_serializer = AttendanceSerializer(data=attendance_data)
            if attendance_serializer.is_valid():
                attendance_serializer.save()

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user_id': user.id,
            'role': user.role,
        })



class RegisterUser(APIView):
    password_salt = 'anfkgzp2201!_asd0Fo__:::SECURITY_HASH_SALTING:0xAFFCBA'
    account_salt = 'DPAD!_saltjoJoad'

    def get(self, request):
        group_list = Group.objects.all()  # Получаем список всех групп
        return render(request, 'register.html', {'group_list': group_list})
    
    def post(self, request):
        # Проверяем, есть ли все необходимые данные
        required_fields = ['user_full_name', 'user_login', 'user_password', 'role', 'group_id']
        missing_fields = [field for field in required_fields if field not in request.data]

        if missing_fields:
            return Response({'error': f'Missing fields: {", ".join(missing_fields)}'}, status=400)

        # Получаем данные из запроса
        user_full_name = request.data['user_full_name']
        user_login = request.data['user_login']
        user_password = request.data['user_password'] + self.password_salt
        role = request.data['role']
        group_id = request.data['group_id']
        telegram_username = request.data.get('telegram_username', '')

        # Хэшируем пароль
        hashed_password = sha256(user_password.encode('utf-8')).hexdigest()

        # Генерируем значение user_hash_value
        user_hash_value = sha256(f'{user_login}{self.account_salt}{user_password}'.encode('utf-8')).hexdigest()

        # Проверяем, что пользователь с таким логином ещё не существует
        if UserModel.objects.filter(user_login=user_login).exists():
            return Response({'error': 'User with this username already exists'}, status=400)

        # Проверяем, существует ли группа с таким ID
        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return Response({'error': 'Group not found'}, status=404)

        # Формируем данные для сериализатора
        user_data = {
            'user_full_name': user_full_name,
            'user_login': user_login,
            'user_password': hashed_password,
            'user_hash_value': user_hash_value,
            'role': role,
            'telegram_username': telegram_username,
        }

        # Используем сериализатор для валидации и сохранения
        serializer = UserModelSerializer(data=user_data)
        if serializer.is_valid():
            user = serializer.save()

            # Создаем запись в StudentProfile
            StudentProfile.objects.create(user=user, group=group)

            # Генерация JWT токенов
            refresh = RefreshToken.for_user(user)

            return Response({
                'message': 'User registered successfully',
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'data': serializer.data,
            }, status=201)
        else:
            return Response({'error': 'Invalid data', 'details': serializer.errors}, status=400)



from django.utils.dateparse import parse_date


from django.db.models import Count

class AttendanceTableView(APIView):
    def get(self, request):
        # Получаем дату из параметров запроса
        date = request.query_params.get('date')
        if not date:
            return Response({"error": "Date parameter is required."}, status=400)
        
        # Преобразуем дату из строки в объект
        date = parse_date(date)
        if not date:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

        # Фильтруем записи посещений по указанной дате
        attendance_records = Attendance.objects.filter(timestamp__date=date)

        # Агрегируем данные
        aggregated_data = AggregatedAttendanceTableSerializer.get_aggregated_data(attendance_records)

        # Подсчет статистики
        total_students = len(aggregated_data)
        on_time_students = sum(1 for record in aggregated_data if record['lateness'] == "")
        late_students = total_students - on_time_students

        # Формируем ответ
        response = {
            "data": aggregated_data,
            "statistics": {
                "total_students": total_students,
                "on_time_students": on_time_students,
                "late_students": late_students,
            }
        }
        return Response(response)
>>>>>>> e6f268d1e21adf5848392f8928c09645e3a08976

class RegisterUserView(generics.CreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = []  # Открываем доступ для всех
