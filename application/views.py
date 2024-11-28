from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .  import models
from . import serializers

class StudentView(generics.ListAPIView):
    def get_queryset(self):
        if 'id' in self.request.query_params:
            return models.Students.objects.filter(user=self.request.query_params['id'])
        return models.Students.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer_for_queryset = serializers.StudentSerializer(queryset, many=True)
        return Response(serializer_for_queryset.data)
    
class TeacherView(generics.ListAPIView):
    def get_queryset(self):
        if 'id' in self.request.query_params:
            return models.Students.objects.filter(user=self.request.query_params['id'])
        return models.Students.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer_for_queryset = serializers.TeacherSerializer(queryset, many=True)
        return Response(serializer_for_queryset.data)
    
class TaskViews(generics.ListAPIView):
    def get_queryset(self):
        if 'id' in self.request.query_params:
            return models.TaskTable.objects.filter(id=self.request.query_params['id'])
        return models.TaskTable.objects.all()
    def get(self,request, *args,**kwargs):
        queryset = self.get_queryset()
        serializers_for_queryset = serializers.TaskSerializers(queryset,many=True)
        return Response(serializers_for_queryset.data)