from django.db import models
from django.utils.text import slugify
import uuid
from application.models import UserModel, Group


class LabWork(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название лабораторной работы")
    description = models.TextField(verbose_name="Описание")
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    open_time = models.DateTimeField(verbose_name="Время открытия")
    close_time = models.DateTimeField(verbose_name="Время закрытия", null=True, blank=True)
    is_open = models.BooleanField(default=True, verbose_name="Открыта")
    allowed_groups = models.ManyToManyField(Group, related_name='allowed_lab_works', verbose_name="Доступные группы")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title+self.description) + '-' + str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class LabWorkResult(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='lab_work_results')
    lab_work = models.ForeignKey(LabWork, on_delete=models.CASCADE, related_name='results')
    date_open = models.DateTimeField(auto_now_add=True, verbose_name="Дата открытия")
    date_answer = models.DateTimeField(null=True, blank=True, verbose_name="Дата ответа")
    open_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP при открытии")
    load_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP при загрузке")
    text_answer = models.TextField(null=True, blank=True, verbose_name="Текстовый ответ")
    grade = models.IntegerField(null=True, blank=True, verbose_name="Оценка")

    def __str__(self):
        return f"{self.user.username} - {self.lab_work.title}"
    

class LabWorkFile(models.Model):
    file = models.FileField(upload_to='lab_work/files', verbose_name="Файл")
    lab_work_result = models.ForeignKey('LabWorkResult', on_delete=models.CASCADE, related_name='files')

    def __str__(self):
        return f"Файл для результата {self.lab_work_result.id}"
    
    
class LabWorkAttachment(models.Model):
    file = models.FileField(upload_to='lab_work/attachments/', verbose_name="Прикрепленный файл")
    lab_work = models.ForeignKey(
        'LabWork',
        on_delete=models.CASCADE,
        related_name='attachments',
        verbose_name="Лабораторная работа"
    )

    def __str__(self):
        return f"Файл для {self.lab_work.title}: {self.file.name}"