import os
import subprocess
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import shutil
import threading
from .models import PypiLibraries

# Функция для скачивания библиотеки
def download_library(library_name, library_path):
    os.makedirs(library_path, exist_ok=True)
    try:
        subprocess.run(
            ['pip', 'download', library_name, '--dest', library_path, '--trusted-host', 'pypi.org', '--trusted-host', 'files.pythonhosted.org'],
            check=True
        )
        print(f'Библиотека "{library_name}" успешно загружена в {library_path}')
    except subprocess.CalledProcessError as e:
        print(f'Ошибка при загрузке библиотеки "{library_name}": {e}')

# Сигнал для автоматической загрузки библиотеки при создании записи
@receiver(post_save, sender=PypiLibraries)
def handle_library_creation(sender, instance, created, **kwargs):
    if created:  # Только при добавлении новой записи
        library_name = instance.name
        library_path = instance.path
        # Запуск загрузки в отдельном потоке
        threading.Thread(target=download_library, args=(library_name, library_path)).start()

# Сигнал для удаления библиотеки при удалении записи
@receiver(post_delete, sender=PypiLibraries)
def handle_library_deletion(sender, instance, **kwargs):
    library_path = instance.path
    if os.path.exists(library_path):
        try:
            shutil.rmtree(library_path)
            print(f'Папка для библиотеки "{instance.name}" удалена')
        except Exception as e:
            print(f'Ошибка при удалении папки для библиотеки "{instance.name}": {e}')
