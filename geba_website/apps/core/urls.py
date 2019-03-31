"""Defines URL patterns for the GEBA website Homepage"""
from django.urls import re_path

from .views import SummernoteUploadAttachment  # import the views module from the directory of this file

urlpatterns = [
    # re_path(r'^$', views.index, name='index'),  # r'^$' -> the base URL for the project\
    re_path(r'^upload_attachment/$', SummernoteUploadAttachment.as_view(),
        name='django_summernote-upload_attachment'),
]
