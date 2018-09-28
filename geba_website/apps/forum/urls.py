"""Defines URL patterns for the GEBA website Blog app"""
from django.urls import re_path
from . import views

urlpatterns = [
    # displays blogs in order from latest to newest

    re_path(r'^$', views.ForumIndexView.as_view(), name='index'),

]
