from django.contrib import admin
from .models import UserModel, Group, StudentProfile, TeacherProfile, Attendance, Task, TaskSubmission, TaskRating, AttendanceRecord

@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ('user_full_name', 'user_login', 'role', 'telegram_username')
    search_fields = ('user_full_name', 'user_login')
    list_filter = ('role',)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'group')
    search_fields = ('user__user_full_name', 'group__name')
    list_filter = ('group',)


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'rank')
    search_fields = ('user__user_full_name', 'rank')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'ip_address', 'timestamp')
    search_fields = ('student__user__user_full_name', 'ip_address')
    list_filter = ('timestamp',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'max_rate')
    search_fields = ('title', 'description')


@admin.register(TaskSubmission)
class TaskSubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'task', 'timestamp')
    search_fields = ('student__user__user_full_name', 'task__title')
    list_filter = ('timestamp',)


@admin.register(TaskRating)
class TaskRatingAdmin(admin.ModelAdmin):
    list_display = ('answer', 'rating')
    search_fields = ('answer__student',)
    list_filter = ('rating',)


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'morning_status', 'lunch_status', 'lateness')
    search_fields = ('student__user__user_full_name', 'date')
    list_filter = ('date',)
