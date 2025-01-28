from django.shortcuts import render
from django.shortcuts import get_object_or_404

from drf_yasg.utils import swagger_auto_schema

from rest_framework import generics, permissions
from .models import LabWork, LabWorkResult
from .serializers import LabWorkSerializer, LabWorkResultSerializer
from application.models import UserModel

class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'teacher'

class LabWorkListCreateView(generics.ListCreateAPIView):
    queryset = LabWork.objects.all()
    serializer_class = LabWorkSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    
    def perform_create(self, serializer):
        serializer.save()
        
    @swagger_auto_schema(
        operation_description="Получить список всех лабораторных работ или создать новую.",
        responses={
            200: LabWorkSerializer(many=True),  # Ответ для GET-запроса
            201: LabWorkSerializer(),  # Ответ для POST-запроса
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Создать новую лабораторную работу.",
        request_body=LabWorkSerializer,  # Тело запроса для POST
        responses={201: LabWorkSerializer()},  # Ответ для успешного создания
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs) 



class LabWorkRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LabWork.objects.all()
    serializer_class = LabWorkSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]
    lookup_field = 'slug'  # Используем slug вместо id

    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(LabWork, slug=slug)
    
    
    
    
class LabWorkResultListCreateView(generics.ListCreateAPIView):
    queryset = LabWorkResult.objects.all()
    serializer_class = LabWorkResultSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    @swagger_auto_schema(
        operation_description="Получить список всех результатов лабораторных работ или создать новый результат.",
        responses={
            200: LabWorkResultSerializer(many=True),  # Ответ для GET-запроса
            201: LabWorkResultSerializer(),  # Ответ для POST-запроса
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Создать новый результат лабораторной работы.",
        request_body=LabWorkResultSerializer,  # Тело запроса для POST
        responses={201: LabWorkResultSerializer()},  # Ответ для успешного создания
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)



class LabWorkResultRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LabWorkResult.objects.all()
    serializer_class = LabWorkResultSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]
    
    @swagger_auto_schema(
        operation_description="Получить детали результата лабораторной работы по ID.",
        responses={200: LabWorkResultSerializer()},  # Ответ для GET-запроса
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Обновить результат лабораторной работы по ID.",
        request_body=LabWorkResultSerializer,  # Тело запроса для PUT/PATCH
        responses={200: LabWorkResultSerializer()},  # Ответ для успешного обновления
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Частично обновить результат лабораторной работы по ID.",
        request_body=LabWorkResultSerializer,  # Тело запроса для PATCH
        responses={200: LabWorkResultSerializer()},  # Ответ для успешного обновления
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Удалить результат лабораторной работы по ID.",
        responses={204: "Результат успешно удален."},  # Ответ для DELETE
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)