"""Defines URL patterns for the GEBA website Homepage"""
from django.urls import re_path

from . import views  # import the views module from the directory of this file

urlpatterns = [
    # re_path(r'^signin/$', views.LoginRegisterFormView.as_view(), name='signin'),

    re_path(r'^register/$', views.RegisterFormView.as_view(), name='register'),

    re_path(r'^login/$', views.LoginFormView.as_view(success_url="/"), name='login'),

    re_path(r'^logout/$', views.logout_view, name='logout'),

]
