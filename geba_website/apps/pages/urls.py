"""Defines URL patterns for the GEBA website Blog app"""
from django.urls import re_path
from . import views

urlpatterns = [

    re_path(r'^contact$', views.ContactView.as_view(), name='contact'),
    re_path(r'^(?P<slug>[\w-]+)$', views.PageDetailView.as_view(), name='detail'),
    re_path(r'^$', views.HomeView.as_view(), name='home'),
    re_path(r'^(?P<slug>[\w-]+)/update/$', views.PageUpdateView.as_view(), name='update')

]
