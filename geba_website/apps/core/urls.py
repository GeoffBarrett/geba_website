"""Defines URL patterns for the GEBA website Homepage"""
from django.urls import re_path

from . import views  # import the views module from the directory of this file

urlpatterns = [
    re_path(r'^$', views.index, name='index'),  # r'^$' -> the base URL for the project
]
