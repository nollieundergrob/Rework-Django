from django.urls import path
from .views import (
    LabWorkListCreateView,
    LabWorkRetrieveUpdateDestroyView,
    LabWorkResultListCreateView,
    LabWorkResultRetrieveUpdateDestroyView,
)

urlpatterns = [
    path('labworks/', LabWorkListCreateView.as_view(), name='labwork-list-create'),
    path('labworks/<slug:slug>/', LabWorkRetrieveUpdateDestroyView.as_view(), name='labwork-retrieve-update-destroy'),
    path('labwork-results/', LabWorkResultListCreateView.as_view(), name='labwork-result-list-create'),
    path('labwork-results/<int:pk>/', LabWorkResultRetrieveUpdateDestroyView.as_view(), name='labwork-result-retrieve-update-destroy'),
]