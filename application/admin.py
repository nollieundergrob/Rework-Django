from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.AnswerTask)
admin.site.register(models.RateTask)
admin.site.register(models.Students)
admin.site.register(models.ReplyAnswer)
admin.site.register(models.StudentsImage)
admin.site.register(models.StudentTag)
admin.site.register(models.StudentsGroups)
admin.site.register(models.TaskTable)
admin.site.register(models.UserModel)
admin.site.register(models.TeacherGroupControl)
admin.site.register(models.TeacherModel)