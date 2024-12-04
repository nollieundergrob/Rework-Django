from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils.timezone import now
from .models import AttendanceRecord, UserModel, Group
from .serializers import AttendanceRecordSerializer, UserSerializer, GroupSerializer,AddUserToGroupSerializer
import logging

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
