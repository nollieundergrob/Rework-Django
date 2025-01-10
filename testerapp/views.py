from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.shortcuts import get_object_or_404
from .models import Test, Question, Answer, Result, Group
from .serializers import (
    TestSerializer, TestCreateSerializer, QuestionSerializer, 
    QuestionCreateSerializer, ResultSerializer, GroupSerializer
)

class IsTeacher(IsAuthenticated):
    """Custom permission for checking if the user is a teacher."""
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_staff

# CRUD для тестов
class TestListCreateView(ListCreateAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TestCreateSerializer
        return TestSerializer

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

class TestDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [IsTeacher]

# CRUD для вопросов
class QuestionListCreateView(ListCreateAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        test_slug = self.kwargs.get('test_slug')
        return Question.objects.filter(test__slug=test_slug)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return QuestionCreateSerializer
        return QuestionSerializer

    def perform_create(self, serializer):
        test = get_object_or_404(Test, slug=self.kwargs.get('test_slug'))
        serializer.save(test=test)

class QuestionDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsTeacher]

# Прохождение теста
class SubmitTestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, test_slug):
        test = get_object_or_404(Test, slug=test_slug, is_active=True)
        user_answers = request.data.get('answers', {})
        total_score = 0
        max_score = 0

        for question in test.questions.all():
            correct_answers = {str(ans.id) for ans in question.answers.filter(is_correct=True)}
            given_answers = set(user_answers.get(str(question.id), []))

            if question.question_type in ['single', 'multiple']:
                max_score += 1
                if correct_answers == given_answers:
                    total_score += 1

        passed = total_score / max_score >= 0.7  # Проходной балл 70%
        result = Result.objects.create(
            user=request.user, test=test, score=total_score / max_score, passed=passed
        )
        return Response({'score': result.score, 'passed': result.passed}, status=status.HTTP_200_OK)
