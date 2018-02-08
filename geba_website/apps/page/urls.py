"""Defines URL patterns for the GEBA website Blog app"""
from django.conf.urls import url, include
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    # displays blogs in order from latest to newest
    # url(r'^$', ListView.as_view(queryset=Post.objects.all().order_by("-created")[:], template_name='blog/detail.html'), name='index'),

    url(r'^$', views.BlogIndexView.as_view(), name='index'),

    # P => named groups <pk> => pk = primary key which is the ID of the Blog post, \d means that the pk is a digit
    # + means that there's 1 or more d's (digits)
    # url(r'^(?P<pk>\d+)$', DetailView.as_view(model=Post, template_name='blog/post.html'))

    url(r'^(?P<slug>[\w-]+)$', views.BlogDetailView.as_view(), name='detail'),

    url(r'^(?P<slug>[\w-]+)/update/$', views.BlogUpdateView.as_view(), name='update'),

    url(r'^create/$', views.BlogCreateView.as_view(), name='create'),

    # url(r'^(?P<pk>\d+)/$', views.BlogUpdateView.as_view(), name='update'),

    url(r'^(?P<slug>[\w-]+)/delete/$', views.BlogDeleteView.as_view(), name='delete'),

    #url(r'^(?q=)$', RedirectView.as_view(url='/')),

]
