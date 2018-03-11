"""Defines URL patterns for the GEBA website Homepage"""
from django.conf.urls import url, include

from . import views  # import the views module from the directory of this file

urlpatterns = [
    url(r'^$', views.index, name='index'),  # r'^$' -> the base URL for the project

    # url(r'^signin/$', views.LoginRegisterFormView.as_view(), name='signin'),

    url(r'^register/$', views.RegisterFormView.as_view(), name='register'),

    url(r'^login/$', views.LoginFormView.as_view(success_url="/"), name='login'),

    url(r'^logout/$', views.logout_view, name='logout'),

]
