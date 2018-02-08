"""Defines URL patterns for the GEBA website Homepage"""
from django.conf.urls import url, include

from . import views  # import the views module from the directory of this file

urlpatterns = [
    url(r'^$', views.AboutMeDetailView.as_view(), name='detail'),  #
]
