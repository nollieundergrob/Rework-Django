from django.db import models
import os
from django.conf import settings

class PypiLibraries(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Имя библиотеки")
    path = models.CharField(max_length=255, blank=True, editable=False, verbose_name="Путь к файлам")
    description = models.TextField(blank=True, verbose_name="Описание", help_text="Краткое описание библиотеки или её предназначение")
    documentation = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Ссылка на документацию")
    def save(self, *args, **kwargs):
        # Генерация пути, если он не установлен
        if not self.path:
            self.path = os.path.join(settings.SIMPLE_LIBS_DIR, self.name)

        # Создание директории для библиотеки
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name
