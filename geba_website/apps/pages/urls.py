"""Defines URL patterns for the GEBA website Blog app"""
from django.urls import re_path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    # redirect /home to the just / because that is where the home.html template lives
    re_path(r'^home$', RedirectView.as_view(url='/', permanent=False)),
    re_path(r'^contact$', views.ContactView.as_view(), name='contact'),
    re_path(r'^(?P<slug>[\w-]+)$', views.PageDetailView.as_view(), name='detail'),
    re_path(r'^$', views.HomeView.as_view(), name='home'),
    re_path(r'^(?P<slug>[\w-]+)/update/$', views.PageUpdateView.as_view(), name='update'),

]
