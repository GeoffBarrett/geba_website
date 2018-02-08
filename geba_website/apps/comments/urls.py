"""Defines URL patterns for the GEBA website Blog app"""
from django.conf.urls import url, include
from django.views.generic import RedirectView
from . import views

urlpatterns = [

    url(r'^(?P<pk>\d+)$', views.CommentThreadView.as_view(), name='thread'),

    url(r'^(?P<pk>\d+)/delete/$', views.CommentDeleteView.as_view(), name='delete'),

    # url(r'^(?P<pk>[\w-]+)/like/$', views.CommentLikeToggle.as_view(), name='like_toggle'),

    url(r'^api/(?P<pk>[\w-]+)/like/$', views.CommentLikeToggleAjax.as_view(), name='like_toggle_api'),

    url(r'^api/(?P<pk>[\w-]+)/dislike/$', views.CommentDislikeToggleAjax.as_view(), name='dislike_toggle_api'),

]
