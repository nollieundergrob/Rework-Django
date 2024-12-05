from django.contrib import admin
from .models import PypiLibraries

@admin.register(PypiLibraries)
class PypiLibrariesAdmin(admin.ModelAdmin):
    list_display = ('name', 'path', 'documentation')
    search_fields = ('name',)
    readonly_fields = ('path',)
