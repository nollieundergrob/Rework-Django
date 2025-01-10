from django.urls import path
from .views import (
    TestListCreateView, TestDetailView, QuestionListCreateView, 
    QuestionDetailView, SubmitTestView
)

urlpatterns = [
    path('', TestListCreateView.as_view(), name='test_list_create'),
    path('<slug:slug>/', TestDetailView.as_view(), name='test_detail'),
    path('<slug:test_slug>/questions/', QuestionListCreateView.as_view(), name='question_list_create'),
    path('<slug:test_slug>/questions/<int:pk>/', QuestionDetailView.as_view(), name='question_detail'),
    path('<slug:test_slug>/submit/', SubmitTestView.as_view(), name='submit_test'),
]
