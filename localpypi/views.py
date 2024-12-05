import os
from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import PypiLibraries
from .serializers import PypiLibrarySerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

class LibraryListView(APIView):
    """
    Возвращает список всех библиотек.
    """
    permission_classes = [AllowAny]
    def get(self, request):
        libraries = PypiLibraries.objects.all()
        if not libraries.exists():
            return Response({'message': 'Список загруженных библиотек пока-что пустой'}, status=status.HTTP_200_OK)
        data = [{'name':item.name,'link':f'http://{request.get_host()}/simple/{item.name}'} for item in libraries]
        return Response(data, status=status.HTTP_200_OK)


class LibraryDetailView(APIView):
    """
    Возвращает детали конкретной библиотеки.
    """
    permission_classes = [AllowAny]
    def get(self, request, name):
        library = get_object_or_404(PypiLibraries, name=name)
        serializer = PypiLibrarySerializer(library, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class LibraryFileDownloadView(APIView):
    """
    Скачивание файла библиотеки.
    """
    permission_classes = [AllowAny]
    def get(self, request, lib_name, filename):
        library = get_object_or_404(PypiLibraries, name=lib_name)
        file_path = os.path.join(library.path, filename)
        if not os.path.exists(file_path):
            return Response({'error': f'Файл "{filename}" не найден в библиотеке "{lib_name}"'}, status=status.HTTP_404_NOT_FOUND)
        return FileResponse(open(file_path, 'rb'), as_attachment=True)
