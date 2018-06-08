"""Defines URL patterns for the GEBA website Blog app"""
from django.urls import re_path
from . import views
# from .forms import ProjectForm, ProjectPostForm


urlpatterns = [

    re_path(r'^$', views.ProjectIndexView.as_view(), name='index'),

    # P => named groups <pk> => pk = primary key which is the ID of the Blog post, \d means that the pk is a digit
    # + means that there's 1 or more d's (digits)
    # re_path(r'^(?P<pk>\d+)$', DetailView.as_view(model=Post, template_name='blog/post.html'))

    re_path(r'^(?P<slug>[\w-]+)/update/$', views.ProjectUpdateView.as_view(), name='update'),
    # re_path(r'^create/$', views.ProjectCreateGetView.as_view(), name='create'),
    re_path(r'^create/$', views.ProjectWizard.as_view(views.TRANSFER_FORMS), name='create'),
    # re_path(r'^create_project/$', views.ProjectCreationPostView.as_view(), name='create_project'),
    # re_path(r'^create_project/$', views.ProjectWizard.as_view([ProjectForm, ProjectPostForm]), name='create_project'),

    re_path(r'^(?P<slug>[\w-]+)/delete/$', views.ProjectDeleteView.as_view(), name='delete'),
    re_path(r'^api/(?P<slug>[\w-]+)/project_like/$', views.ProjectLikeToggleAjax.as_view(),
            name='project_like_toggle_api'),
    re_path(r'^api/(?P<slug>[\w-]+)/project_dislike/$', views.ProjectDislikeToggleAjax.as_view(),
        name='project_dislike_toggle_api'),

    #  -------------------Project Post URLS ------------------
    # re_path(r'^api/create_project_post/$', views.ProjectPostCreationPostViewAjax.as_view(),
    # name='create_project_post_ajax'),

    re_path(r'^create_project_post/$', views.ProjectPostCreationPostView.as_view(), name='create_project_post'),

    re_path(r'^(?P<slug>[\w-]+)/update_post/$', views.ProjectPostUpdateView.as_view(), name='update_post'),
    re_path(r'^(?P<slug>[\w-]+)/(?P<post_order>[0-9]+)/create_post/$', views.ProjectPostCreateView.as_view(),
        name='create_post'),
    re_path(r'^(?P<slug>[\w-]+)/delete_post/$', views.ProjectPostDeleteView.as_view(), name='delete_post'),

    re_path(r'^api/(?P<slug>[\w-]+)/like/$', views.ProjectPostLikeToggleAjax.as_view(), name='post_like_toggle_api'),
    re_path(r'^api/(?P<slug>[\w-]+)/dislike/$', views.ProjectPostDislikeToggleAjax.as_view(),
            name='post_dislike_toggle_api'),

    #  ---------------------- Both  ---------------------------------

    re_path(r'^(?P<slug>[\w-]+)$', views.ProjectDetailView.as_view(), name='detail'),

    #  --------------------  draft / publish  -----------------------------
    re_path(r'^api/(?P<slug>[\w-]+)/publish_post/$', views.PublishProjectPostAjax.as_view(), name='publish_post_ajax'),

    re_path(r'^api/(?P<slug>[\w-]+)/draft_post/$', views.MakeDraftProjectPostAjax.as_view(), name='draft_post_ajax'),

    re_path(r'^api/(?P<slug>[\w-]+)/publish/$', views.PublishProjectAjax.as_view(), name='publish_project_ajax'),

    re_path(r'^api/(?P<slug>[\w-]+)/draft/$', views.MakeDraftProjectAjax.as_view(), name='draft_project_ajax'),

]
