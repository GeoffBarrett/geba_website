"""Defines URL patterns for the GEBA website Blog app"""
from django.conf.urls import url
from . import views

urlpatterns = [
    # displays blogs in order from latest to newest

    url(r'^$', views.ProjectIndexView.as_view(), name='index'),

    # P => named groups <pk> => pk = primary key which is the ID of the Blog post, \d means that the pk is a digit
    # + means that there's 1 or more d's (digits)
    # url(r'^(?P<pk>\d+)$', DetailView.as_view(model=Post, template_name='blog/post.html'))

    url(r'^(?P<slug>[\w-]+)/update/$', views.ProjectUpdateView.as_view(), name='update'),
    url(r'^create/$', views.ProjectCreateGetView.as_view(), name='create'),
    url(r'^create_project/$', views.ProjectCreationPostView.as_view(), name='create_project'),
    url(r'^(?P<slug>[\w-]+)/delete/$', views.ProjectDeleteView.as_view(), name='delete'),
    url(r'^api/(?P<slug>[\w-]+)/project_like/$', views.ProjectLikeToggleAjax.as_view(), name='project_like_toggle_api'),
    url(r'^api/(?P<slug>[\w-]+)/project_dislike/$', views.ProjectDislikeToggleAjax.as_view(),
        name='project_dislike_toggle_api'),

    ####################Project Post URLS#####################

    url(r'^(?P<slug>[\w-]+)/update_post/$', views.ProjectPostUpdateView.as_view(), name='update_post'),
    url(r'^(?P<slug>[\w-]+)/(?P<post_order>[0-9]+)/create_post/$', views.ProjectPostCreateView.as_view(),
        name='create_post'),
    url(r'^(?P<slug>[\w-]+)/delete_post/$', views.ProjectPostDeleteView.as_view(), name='delete_post'),

    url(r'^api/(?P<slug>[\w-]+)/like/$', views.ProjectPostLikeToggleAjax.as_view(), name='post_like_toggle_api'),
    url(r'^api/(?P<slug>[\w-]+)/dislike/$', views.ProjectPostDislikeToggleAjax.as_view(), name='post_dislike_toggle_api'),

    ####################### Both ###################################

    url(r'^(?P<slug>[\w-]+)$', views.ProjectDetailView.as_view(), name='detail'),

]
