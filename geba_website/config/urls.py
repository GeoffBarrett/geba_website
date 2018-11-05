"""geba_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import re_path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from django.views.generic import RedirectView


handler404 = 'apps.pages.views.handler404'
handler500 = 'apps.pages.views.handler500'
handler403 = 'apps.pages.views.handler403'
handler400 = 'apps.pages.views.handler400'

urlpatterns = [
    # -------------------- social link redirects -------------------------------
    re_path(r'^youtube$', RedirectView.as_view(url='https://www.youtube.com/channel/UCoTtKQQhQHXMpCBSINlpO-A',
                                               permanent=False)),
    re_path(r'^github$', RedirectView.as_view(url='https://www.github.com/GeoffBarrett', permanent=False)),
    re_path(r'^twitter$', RedirectView.as_view(url='http://twitter.com/geba_tech', permanent=False)),
    re_path(r'^linkedin$', RedirectView.as_view(url='https://www.linkedin.com/in/gmbarrett', permanent=False)),

    # --------- custom urls ---------------------- #
    re_path(r'^', include(('apps.pages.urls', "pages"))),
    re_path(r'^auth/', include(('apps.geba_auth.urls', "geba_auth"))),  # geba_auth app
    re_path(r'^analytics/', include(('apps.geba_analytics.urls', "geba_analytics"))),  # geba_analytics app
    re_path(r'^blog/', include(('apps.blog.urls', "blog"))),  # Blog app
    re_path(r'^polls/', include(('apps.polls.urls', "polls"))),
    re_path(r'^comments/', include(('apps.comments.urls', "comments"))),
    re_path(r'^project/', include(('apps.project.urls', "project"))),
    re_path(r'^forum/', include(('apps.forum.urls', "forum"))),  # Blog app

    # ------------ third party urls -------------------- #
    re_path(r'^grappelli/', include('grappelli.urls')),  # grappelli URLS
    re_path(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^summernote/', include('django_summernote.urls')),
    # re_path(r'^tinymce/', include('tinymce.urls')),
    # re_path(r'^comments/', include('django_comments.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
