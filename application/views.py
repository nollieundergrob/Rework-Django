import json
from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from .models import UserModel, Group, StudentProfile, TeacherProfile, Task
from .serializers import (
    AttendanceSerializer,
    UserModelSerializer,
    GroupSerializer,
    StudentProfileSerializer,
    TeacherProfileSerializer,
    TaskSerializer,
    
)
from . import utils
from django.http import *
from hashlib import sha256
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views import View
import datetime
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


# CRUD для пользователей
class UserModelView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = UserModel.objects.all()
    serializer_class = UserModelSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# CRUD для групп
class GroupView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

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


class LoginUser(View):
    salt = 'anfkgzp2201!_asd0Fo__:::SECURITY_HASH_SALTING:0xAFFCBA'
    def get(self,request):
        return render(request,'login.html')
    def post(self,request):
        if 'login' in request.POST and 'password' in request.POST:
            login = request.POST['login']
            password = request.POST['password']+self.salt
            hashed_password = sha256(password.encode('utf-8')).hexdigest()
            Hash_account = sha256(f'{login}DPAD!_saltjoJoad{password}'.encode('utf-8')).hexdigest()
            print(Hash_account,hashed_password)
            Find_login = UserModel.objects.filter(user_hash_value=Hash_account).first()
            if not Find_login:
                return JsonResponse({'error': 'Не найден такой аккаунт'}, status=404)

            # Логирование входа
            ip_address = utils.get_root_ip(request)
            user_agent = request.headers.get('User-Agent', '')
            # Если пользователь — студент, создаём запись посещения
            attendance_data = {
                    'student': Find_login.id,  # Идентификатор пользователя
                    'ip_address': ip_address,
                    'user_agent': json.dumps({'user_agent': user_agent}),
                    'timestamp': datetime.datetime.now()
                }
            if Find_login and Find_login.role == 'student':
                attendance_serializer = AttendanceSerializer(data=attendance_data)
                if attendance_serializer.is_valid():
                    attendance_serializer.save()
                else:
                    print("Ошибка логирования посещения:", attendance_serializer.errors)

            # Установка куки и возврат токена
            response = JsonResponse(attendance_data)
            response.set_cookie('auth_token', Hash_account, max_age=60 * 60 * 3)
            return response


class RegisterUser(View):
    password_salt = 'anfkgzp2201!_asd0Fo__:::SECURITY_HASH_SALTING:0xAFFCBA'
    account_salt = 'DPAD!_saltjoJoad'

    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        # Проверяем, есть ли все необходимые данные
        required_fields = ['user_full_name', 'user_login', 'user_password', 'role']
        missing_fields = [field for field in required_fields if field not in request.POST]

        if missing_fields:
            return JsonResponse({'error': f'Missing fields: {", ".join(missing_fields)}'}, status=400)

        # Получаем данные из POST-запроса
        user_full_name = request.POST['user_full_name']
        user_login = request.POST['user_login']
        user_password = request.POST['user_password'] + self.password_salt
        role = request.POST['role']
        telegram_username = request.POST.get('telegram_username', '')

        # Хэшируем пароль
        hashed_password = sha256(user_password.encode('utf-8')).hexdigest()

        # Генерируем значение user_hash_value
        user_hash_value = sha256(f'{user_login}{self.account_salt}{user_password}'.encode('utf-8')).hexdigest()

        # Проверяем, что пользователь с таким логином ещё не существует
        if UserModel.objects.filter(user_login=user_login).exists():
            return JsonResponse({'error': 'User with this username already exists'}, status=400)

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
            serializer.save()
            return JsonResponse({'message': 'User registered successfully', 'data': serializer.data}, status=201)
        else:
            return JsonResponse({'error': 'Invalid data', 'details': serializer.errors}, status=400)

