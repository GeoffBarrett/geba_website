"""Defines URL patterns for the GEBA website Blog app"""
from django.urls import re_path
# from django.views.generic import RedirectView
from . import views

urlpatterns = [

    re_path(r'^(?P<pk>\d+)$', views.CommentThreadView.as_view(), name='thread'),

    re_path(r'^(?P<pk>\d+)/delete/$', views.CommentDeleteView.as_view(), name='delete'),

    # url(r'^(?P<pk>[\w-]+)/like/$', views.CommentLikeToggle.as_view(), name='like_toggle'),

    re_path(r'^api/(?P<pk>[\w-]+)/like/$', views.CommentLikeToggleAjax.as_view(), name='like_toggle_api'),

    re_path(r'^api/(?P<pk>[\w-]+)/dislike/$', views.CommentDislikeToggleAjax.as_view(), name='dislike_toggle_api'),

]
