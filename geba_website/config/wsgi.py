"""
WSGI config for geba_website project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings.production"
# os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings.staging"


from django.core.wsgi import get_wsgi_application, WSGIHandler
application = get_wsgi_application()
# application = WSGIHandler()
