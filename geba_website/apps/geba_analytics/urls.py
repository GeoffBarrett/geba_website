"""Defines URL patterns for the GEBA website Blog app"""
from django.urls import re_path
from . import views

urlpatterns = [
    # displays blogs in order from latest to newest
    re_path(r'^$', views.AnalyticsView.as_view(), name='home'),
    re_path(r'^api/data$', views.AnalyticsData.as_view(), name='api-data'),

]
