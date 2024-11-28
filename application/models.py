from django.db import models
import datetime
import hashlib



class UserModel(models.Model):
    """
    Модель пользователя
    """
    user_full_name = models.CharField('ФИО студента',max_length=100)
    user_login = models.CharField('username',max_length=100)
    user_hash_value = models.CharField(db_index=True, max_length=65)
    user_password = models.CharField(max_length=32)
    user_telegram_username = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.user_full_name} ({self.user_telegram_username})'


# Students Models
class StudentsGroups(models.Model):
    student_group = models.CharField(max_length=128)
    def __str__(self):
        return self.student_group
    
    

class Students(models.Model):
    user = models.ForeignKey(UserModel,on_delete=models.CASCADE,related_name='student')
    student_group = models.ForeignKey(StudentsGroups,on_delete=models.CASCADE,related_name='group')
    def __str__(self):
        return f'{self.student_group} {self.user}'

class StudentsImage(models.Model):
    student = models.ForeignKey(Students,on_delete=models.CASCADE,related_name='photo')
    studnet_image = models.ImageField(upload_to='media/students')

class StudentTag(models.Model):
    tag_student = models.ForeignKey(Students,on_delete=models.CASCADE,related_name='tag')
    tag_ip = models.CharField(max_length=16)
    tag_date = models.CharField(default=str(datetime.datetime.now().strftime("%d.%m.%Y")), max_length=100 )
    tag_time = models.CharField(default=str(datetime.datetime.now().strftime("%H:%M")), max_length=100 )\


#Teacher Models
class TeacherModel(models.Model):
    user = models.ForeignKey(UserModel,on_delete=models.CASCADE,related_name='user')
    rank = models.CharField(max_length=64)

class TeacherGroupControl(models.Model):
    teacher = models.ForeignKey(TeacherModel,on_delete=models.CASCADE,related_name='teacher_field')
    control = models.ForeignKey(StudentsGroups,on_delete=models.CASCADE,related_name='teacher_ctrl')

# Tasks Models
class TaskTable(models.Model):
    """ Таблица для создания заданий.
        Поля:
        Заголовок;
        Описание;
        Хэш-значение;
        Статус;
    """
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=512)
    hash_value = models.CharField(max_length=65)
    status = models.BooleanField(default=True)
    max_rate = models.IntegerField()
    # STATUSES:
    # 0 - closed
    # 1 - opened

class TaskImages(models.Model):
    taskid = models.ForeignKey(TaskTable, on_delete=models.CASCADE, related_name='photo')
    photo = models.ImageField(upload_to='media/tasks/images')
    

class AnswerTask(models.Model):
    student = models.ForeignKey(Students,on_delete=models.CASCADE,related_name='student')
    task = models.ForeignKey(TaskTable,on_delete=models.CASCADE,related_name='answers')
    file = models.FileField(verbose_name='Answer task', upload_to='media/task/files')
    date_answer = models.CharField(default=str(datetime.datetime.now().strftime("%d.%m.%Y")), max_length=100 )
    time_answer = models.CharField(default=str(datetime.datetime.now().strftime("%H:%M")), max_length=100)
    

class ReplyAnswer(models.Model):
    answer = models.ForeignKey(AnswerTask,on_delete=models.CASCADE)
    text = models.CharField(max_length=512)

class RateTask(models.Model):
    task = models.ForeignKey(TaskTable, on_delete=models.CASCADE, related_name='rate')
    rate = models.IntegerField()




