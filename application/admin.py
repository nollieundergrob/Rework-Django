from django.contrib import admin
<<<<<<< HEAD
from .models import UserModel, Group, AttendanceRecord

=======
from .models import UserModel, Group, StudentProfile, TeacherProfile, Attendance, Task, TaskSubmission, TaskRating
>>>>>>> e6f268d1e21adf5848392f8928c09645e3a08976

@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    """
    Админка для модели UserModel.
    """
    list_display = ('username', 'first_name', 'last_name', 'role', 'telegram_username')
    list_filter = ('role',)
    search_fields = ('username', 'first_name', 'last_name', 'telegram_username')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """
    Админка для модели Group.
    """
    list_display = ('name',)
    search_fields = ('name',)
<<<<<<< HEAD
    filter_horizontal = ('teachers', 'students')


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    """
    Админка для модели AttendanceRecord.
    """
    list_display = ('user', 'timestamp', 'ip_address', 'request_method', 'request_url')
    list_filter = ('timestamp', 'request_method')
    search_fields = ('user__username', 'ip_address', 'request_url')
    date_hierarchy = 'timestamp'
=======


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
>>>>>>> e6f268d1e21adf5848392f8928c09645e3a08976
