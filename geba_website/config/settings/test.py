"""
Django settings for geba_website testing

This will use the local  database while using S3
"""
from .base import *

# from os import environ

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# -------------------- HOST CONFIGURATION ----------------------- #
# See: https://docs.djangoproject.com/en/1.5/releases/1.5/#allowed-hosts-required-in-production
ALLOWED_HOSTS = ['geba.technology', 'www.geba.technology', '127.0.0.1', get_secret('host_ip')]
# ---------------- END HOST CONFIGURATION --------------------- #

# ------------- EMAIL CONFIGURATION -------------------- #
# https://docs.djangoproject.com/en/dev/ref/settings/#email-use-tls
EMAIL_USE_TLS = True

# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# https://docs.djangoproject.com/en/dev/ref/settings/#default-from-email
DEFAULT_FROM_EMAIL = 'geoff@geba.technology'

# https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = 'smtp.gmail.com'

# https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = 587

# https://docs.djangoproject.com/en/dev/ref/settings/#email-host-user
EMAIL_HOST_USER = 'geoff@geba.technology'

# https://docs.djangoproject.com/en/dev/ref/settings/#email-host-password
EMAIL_HOST_PASSWORD = get_secret('gmail_password')
# --------------- END EMAIL CONFIGURATION --------------- #


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

# ------------------- CACHE CONFIGURATION --------------------#
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
# ------------------ END CACHE CONFIGURATION --------------------- #

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# ------------------ analytics settings ---------------------- #

CLICKY_SITE_ID = get_secret('CLICKY_SITE_ID')
CRAZY_EGG_ACCOUNT_NUMBER = 'xxxxxxxx'

ANALYTICAL_INTERNAL_IPS = ['192.XXX.X.XX']
GOOGLE_ANALYTICS_PROPERTY_ID = get_secret('GOOGLE_ANALYTICS_PROPERTY_ID')
GOOGLE_ANALYTICS_DISPLAY_ADVERTISING = True
GOOGLE_ANALYTICS_SITE_SPEED = True

# ------------------- end of analytics settings --------------- #

# ------------------- amazon aws s3 ----------------- #
# the sub-directories of media and static files

# s3 = boto3.resource('s3')

STATICFILES_LOCATION = 'static'
MEDIAFILES_LOCATION = 'media'

S3_USE_SIGV4 = True

# if False it will create unique file names for every uploaded file
AWS_S3_FILE_OVERWRITE = False

AWS_STORAGE_BUCKET_NAME = get_secret('AWS_STORAGE_BUCKET_NAME')
AWS_ACCESS_KEY_ID = get_secret('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = get_secret('AWS_SECRET_ACCESS_KEY')

# This will make sure that the file URL does not have unnecessary parameters like your access key.

AWS_QUERYSTRING_AUTH = False

# Tell django-storages that when coming up with the URL for an item in S3 storage, keep
# it simple - just use this domain plus the path. (If this isn't set, things get complicated).
# This controls how the `static` template tag from `staticfiles` gets expanded, if you're using it.
# We also use it in the next setting.
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

AWS_HEADERS = {  # see http://developer.yahoo.com/performance/rules.html#expires
        'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
        'Cache-Control': 'max-age=94608000',
}

# a custom storage file, so we can easily put static and media in one bucket
STATICFILES_STORAGE = 'apps.core.custom_storages.StaticStorage'
DEFAULT_FILE_STORAGE = 'apps.core.custom_storages.MediaStorage'

STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)

ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)

# --------------- end of amazon --------------------------- #
