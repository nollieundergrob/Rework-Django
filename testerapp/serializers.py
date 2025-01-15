from rest_framework import serializers
from .models import Test, Question, Answer, Result, Group
from application.serializers import GroupSerializer

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'answer_text', 'is_correct']

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'question_type', 'answers']

class QuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['question_text', 'question_type']

class TestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = Test
        fields = ['id', 'name', 'description', 'is_active', 'slug', 'groups', 'questions']

class TestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['name', 'description', 'is_active', 'groups']

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ['user', 'test', 'score', 'passed', 'completed_at']
