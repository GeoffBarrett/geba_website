"""Defines URL patterns for the GEBA website Homepage"""
from django.urls import re_path

from . import views  # import the views module from the directory of this file

urlpatterns = [

    re_path(r'^register/$', views.RegisterFormView.as_view(), name='register'),

    re_path(r'^resend_activation/$', views.ResendActivationFormView.as_view(), name='resend_act'),

    re_path(r'^forgot_password/$', views.ForgotPasswordFormView.as_view(), name='forgot_password'),

    re_path(r'^login/$', views.LoginFormView.as_view(success_url="/"), name='login'),

    re_path(r'^logout/$', views.logout_view, name='logout'),

    re_path(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),

    re_path(r'^account_activation_invalid/$', views.account_activation_invalid, name='account_activation_invalid'),

    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            views.activate, name='activate'),

    re_path(r'^reset_password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                views.reset_password.as_view(), name='reset_password'),


]
