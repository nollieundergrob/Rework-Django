from django.urls import path
from . import views

urlpatterns = [
    path('', views.LibraryListView.as_view(), name='get_libraries'),
    path('<str:name>/', views.LibraryDetailView.as_view(), name='library_dispatcher'),
    path('<str:lib_name>/<str:filename>/', views.LibraryFileDownloadView.as_view(), name='download_library_file'),
]
