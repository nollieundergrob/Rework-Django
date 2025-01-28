from rest_framework import serializers
from .models import LabWork, LabWorkResult, LabWorkFile, LabWorkAttachment
from application.serializers import *

class LabWorkFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabWorkFile
        fields = ['id', 'file']


class LabWorkResultSerializer(serializers.ModelSerializer):
    files = LabWorkFileSerializer(many=True, read_only=True)
    file_uploads = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,
        required=False,
    )

    class Meta:
        model = LabWorkResult
        fields = ['id', 'user', 'lab_work', 'date_open', 'date_answer', 'open_ip', 'load_ip', 'text_answer', 'grade', 'files', 'file_uploads']

    def create(self, validated_data):
        file_uploads = validated_data.pop('file_uploads', [])
        lab_work_result = super().create(validated_data)

        for file in file_uploads:
            LabWorkFile.objects.create(lab_work_result=lab_work_result, file=file)

        return lab_work_result

    def update(self, instance, validated_data):
        file_uploads = validated_data.pop('file_uploads', [])
        lab_work_result = super().update(instance, validated_data)

        for file in file_uploads:
            LabWorkFile.objects.create(lab_work_result=lab_work_result, file=file)

        return lab_work_result
        

class LabWorkAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabWorkAttachment
        fields = ('id', 'file')

class LabWorkSerializer(serializers.ModelSerializer):
    results = LabWorkResultSerializer(many=True, read_only=True)  
    attachments = LabWorkAttachmentSerializer(many=True, read_only=True) 
    allowed_groups = GroupSerializer(many=True, read_only=True)  

    class Meta:
        model = LabWork
        fields = [
            'id', 
            'title', 
            'description', 
            'slug', 
            'open_time', 
            'close_time', 
            'is_open', 
            'allowed_groups',
            'attachments', 
            'results'  
        ]





