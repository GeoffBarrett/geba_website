"""Defines URL patterns for the GEBA website Blog app"""
from django.urls import re_path
from . import views

urlpatterns = [

    re_path(r'^(?P<slug>[\w-]+)$', views.PageDetailView.as_view(), name='detail'),
    re_path(r'^$', views.HomeView.as_view(), name='home')

]
