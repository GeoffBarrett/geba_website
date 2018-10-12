"""
Django settings for geba_website project.

Generated by 'django-admin startproject' using Django 1.10.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""
from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

# default => 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # sendgrid
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'geoff@geba.technology'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'geoff@geba.technology'
# EMAIL_HOST_PASSWORD = get_env_variable('sendgrid_password')
EMAIL_HOST_PASSWORD = get_env_variable('gmail_password')

# SITE_ID = 1

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': "geba_website",
        'USER': 'Geoff',
        'PASSWORD': get_env_variable('database_password'),
        'HOST': 'localhost',
        'PORT': '',
    }
}


########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
########## END CACHE CONFIGURATION

INSTALLED_APPS += ('debug_toolbar',)

MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
# see the amazon section, if commented out
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
# this is where all the files will be put with collectstatic
STATIC_ROOT = os.path.normpath(os.path.join(DJANGO_ROOT, 'static'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'  # where you put all your webapp static files webappname/static_url/

# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
# see the amazon section, if commented out
# Absolute filesystem path to the directory that will hold geba_auth-uploaded files.
MEDIA_ROOT = os.path.normpath(os.path.join(DJANGO_ROOT, 'media'))

# URL that handles the media served from MEDIA_ROOT, used for managing stored files.
MEDIA_URL = '/media/'

CACHE_TIMEOUT = 30
