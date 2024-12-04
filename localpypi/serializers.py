from rest_framework import serializers
from .models import PypiLibraries
import os
class PypiLibrarySerializer(serializers.ModelSerializer):
    install_command = serializers.SerializerMethodField()

    class Meta:
        model = PypiLibraries
        fields = ['id', 'name', 'description', 'documentation', 'install_command']

    def get_install_command(self, obj):
        """
        Формирование команды установки библиотеки через pip.
        """
        if obj.path and os.path.exists(obj.path):
            files = os.listdir(obj.path)
            file_urls = [
                f"{self.context['request'].build_absolute_uri('/simple/')}{obj.name}/{file}"
                for file in files
            ]
            return f"pip install {' '.join(file_urls)} --no-deps"
        return None
