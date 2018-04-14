"""Defines URL patterns for the GEBA website Blog app"""
from django.urls import re_path
from . import views

urlpatterns = [
    # displays blogs in order from latest to newest

    re_path(r'^$', views.BlogIndexView.as_view(), name='index'),

    # P => named groups <pk> => pk = primary key which is the ID of the Blog post, \d means that the pk is a digit
    # + means that there's 1 or more d's (digits)
    # url(r'^(?P<pk>\d+)$', DetailView.as_view(model=Post, template_name='blog/post.html'))

    re_path(r'^(?P<slug>[\w-]+)$', views.BlogDetailView.as_view(), name='detail'),

    re_path(r'^(?P<slug>[\w-]+)/update/$', views.BlogUpdateView.as_view(), name='update'),

    re_path(r'^create/$', views.BlogCreateView.as_view(), name='create'),

    re_path(r'^(?P<slug>[\w-]+)/delete/$', views.BlogDeleteView.as_view(), name='delete'),

    re_path(r'^api/(?P<slug>[\w-]+)/like/$', views.PostLikeToggleAjax.as_view(), name='like_toggle_api'),

    re_path(r'^api/(?P<slug>[\w-]+)/dislike/$', views.PostDislikeToggleAjax.as_view(), name='dislike_toggle_api'),

    re_path(r'^api/(?P<slug>[\w-]+)/publish/$', views.PublishPostAjax.as_view(), name='publish_ajax'),

    re_path(r'^api/(?P<slug>[\w-]+)/draft/$', views.MakeDraftPostAjax.as_view(), name='draft_ajax'),

]
