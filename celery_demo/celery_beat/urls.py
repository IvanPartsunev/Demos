from django.urls import path

from celery_demo.celery_beat.views import DataView

urlpatterns = [
    path("", DataView.as_view(), name="data"),
]
