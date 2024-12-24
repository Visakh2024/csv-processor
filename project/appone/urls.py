# app.urls
from django.urls import path
from .views import UploadCSVAPIView

urlpatterns = [
    path('upload-csv/', UploadCSVAPIView.as_view(), name='upload-csv'),  # API endpoint
    path('upload-form/', UploadCSVAPIView.as_view(), name='upload-form'),  # For testing via the form
]
