from django.urls import path,include
from . import views


student_patterns = [
    path('students/', views.StudentView.as_view(), name='student-list'),
]
teacher_patterns = [
    path('teachers/',view=views.TeacherView.as_view())
]
task_pattern = [
    path('tasks/',view=views.TaskViews.as_view())
]
urlpatterns = [
    # path('users/', views.UserView.as_view(), name='user-list'),
] + student_patterns + teacher_patterns + task_pattern