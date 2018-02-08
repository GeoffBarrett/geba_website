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
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from django.views.generic import RedirectView

urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),  # grappelli URLS
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('apps.core.urls', namespace="core")),  # Home app
    url(r'^about/', include('apps.about_me.urls', namespace="about")),  # About Me app
    url(r'^blog/', include('apps.blog.urls', namespace="blog")),  # Blog app
    url(r'^polls/', include('apps.polls.urls', namespace="polls")),
    url(r'^comments/', include('apps.comments.urls', namespace="comments")),
    url(r'^project/', include('apps.project.urls', namespace="project")),

    # -------------------- social link redirects -------------------------------
    url(r'^youtube/', RedirectView.as_view(url='https://www.youtube.com/channel/UCoTtKQQhQHXMpCBSINlpO-A', permanent=False)),
    url(r'^twitter/', RedirectView.as_view(url='http://twitter.com/geba_tech', permanent=False)),
    url(r'^linkedin/', RedirectView.as_view(url='https://www.linkedin.com/in/gmbarrett', permanent=False))

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
