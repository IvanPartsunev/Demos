from django.urls import path

from celery_demo.project_core.views import UploadImageView, ImageUploadView

urlpatterns = [
    path("", UploadImageView.as_view(), name="upload_image"),
    path("uploaded/", ImageUploadView.as_view(), name="uploaded"),
]
