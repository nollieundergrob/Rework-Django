from django.contrib import admin
from .models import UserModel, Group, AttendanceRecord,AttendanceFile

@admin.register(AttendanceFile)
class AttendanceFileAdmin(admin.ModelAdmin):
    """
    Админка для модели AttendanceFile.
    """
    list_display = ('user', 'date', 'file')  # Отображение пользователя, даты и файла
    search_fields = ('date', 'user__username')  # Поиск по дате и имени пользователя
    list_filter = ('date', 'user')  # Фильтрация по дате и пользователю




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
