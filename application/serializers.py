from rest_framework import serializers
from . import models



#Base Serializers
 
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserModel
        fields = ('user_full_name','user_login','user_hash_value','user_password','user_telegram_username')

class TaskImageSerializers(serializers.ModelSerializer):
    class Meta:
        model= models.TaskImages
        fields = ('photo',)
class ReplyTaskSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.ReplyAnswer
        fields = ('text',)

class GroupSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.StudentsGroups
        fields = ('group',)

class StudentImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.StudentsImage
        fields = ('studnet_image',)


#Modify Serailizers


##Students Serializers
class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    photo = StudentImageSerializers(many=True,read_only=True)
    class Meta:
        model = models.Students
        fields = ('user','student_group','photo')


class StudentTag(serializers.ModelSerializer):

    class Meta:
        model = models.StudentTag
        fields = ('student','ip','date','time')

##Task Serializers    
class AnswerTask(serializers.ModelSerializer):
    reply = ReplyTaskSerializers(many=True,read_only=True)
    class Meta:
        model = models.AnswerTask
        fields = ('student','task','file','date_answer','time_answer','date_answer','reply')

class TaskSerializers(serializers.ModelSerializer):
    images = TaskImageSerializers(many=True,read_only=True)
    answers = AnswerTask(many=True,read_only=True)
    class Meta:
        model = models.TaskTable
        fields = ('title','description','hash_value','max_rate','status','answers','images')


# Teacher Serializers
class TeacherControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TeacherGroupControl
        fields = ['control',]
    
class TeacherSerializer(serializers.ModelSerializer):
    control = TeacherControlSerializer(read_only=True) 

    class Meta:
        model = models.TeacherModel
        fields = ['user','control']