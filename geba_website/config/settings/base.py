"""
Django settings for geba_website project.

Generated by 'django-admin startproject' using Django 1.10.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""
import os
from sys import path
from unipath import Path
import json
from django.core.exceptions import ImproperlyConfigured


def get_env_variable(var_name):
    try:
        # return os.environ[var_name]
        return os.environ.get(var_name)
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name
        raise ImproperlyConfigured(error_msg)


DJANGO_ROOT = Path(__file__).ancestor(3)  # /geba_website/geba_website

secrets_filename = os.path.join(DJANGO_ROOT, 'secrets.json')

with open(secrets_filename) as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the %s environment variable" % setting
        raise ImproperlyConfigured(error_msg)


CONFIG_ROOT = DJANGO_ROOT.child("config")

APPS_DIR = DJANGO_ROOT.child("apps")

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
path.append(DJANGO_ROOT)

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = False


# A list of all the people who get code error notifications.
ADMINS = (
    ('Geoffrey Barrett', 'geoff@geba.technology')
)

MANAGERS = ADMINS


DATABASES = {
    'default': {
        'ENGINE': '',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'ATOMIC_REQUESTS': True,  # use this until performance overhead becomes unbearable
    }

}
# end database config #####

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

# We will use UTC timezones, makes it easier on conversions
TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# MEDIA CONFIGURATION
# see the amazon section, if commented out
# Absolute filesystem path to the directory that will hold geba_auth-uploaded files.
# MEDIA_ROOT = os.path.normpath(os.path.join(DJANGO_ROOT, 'media'))

# URL that handles the media served from MEDIA_ROOT, used for managing stored files.
# MEDIA_URL = '/media/'
# END MEDIA CONFIGURATION

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
# see the amazon section, if commented out
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
# this is where all the files will be put with collectstatic
# STATIC_ROOT = os.path.normpath(os.path.join(DJANGO_ROOT, 'static'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
# STATIC_URL = '/static/'  # where you put all your webapp static files webappname/static_url/

# these folders are those that will also be loaded in {% load staticfiles %}
STATICFILES_DIRS = (
    os.path.normpath(os.path.join(DJANGO_ROOT, 'assets')),
)

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# SECURITY WARNING: keep the secret key used in production secret!

# when using uWSGI the environmental variables didn't work so I stored variables in a secretes.json file
# SECRET_KEY = get_env_variable("secret_key")
SECRET_KEY = get_secret("secret_key")

# A list of strings representing the host/domain names that this Django site can serve.
# This is a security measure to prevent HTTP Host header attacks, which are possible even under many seemingly-safe
# web server configurations.
#  A value beginning with a period can be used as a subdomain wildcard
ALLOWED_HOSTS = []

# Application definition

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)


THIRD_PARTY_APPS = (
    'analytical',
    # 'authtools',
    'crispy_forms',
    # 'django_extensions',
    # 'django_rq',
    'django_summernote',
    # 'floppyforms',
    'filebrowser',
    'formtools',
    'grappelli',
    'markdown_deux',
    # 'pagedown',  # this is for the pagedown WYSIWYG editor
    # 'pipeline',
    'rest_framework',
    'storages',
    'tinymce',  # another WYSIWYG editor
)

# usually I would put these in 3rd party, but I need them in a specific order
THREADEDCOMMENTS_APPS = (
    'django_comments',
    'django.contrib.sites',
)

PROJECT_APPS = (
    'apps.blog',  # the Blog app
    'apps.comments',
    'apps.core',  # adding the core page to the settings
    'apps.forum',
    'apps.geba_analytics',
    'apps.geba_auth',
    'apps.keyword',
    'apps.pages',
    'apps.polls',
    'apps.profiles',
    'apps.project',
    'apps.vote',
)


CSRF_USE_SESSIONS = False  # Djangos's default

##########################

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS + THREADEDCOMMENTS_APPS

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# A string representing the full Python import path to your root URLconf. For example: "mydjangoapps.urls".
ROOT_URLCONF = 'config.urls'

# A list containing the settings for all template engines to be used with Django
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.normpath(os.path.join(DJANGO_ROOT, 'templates')),
                 ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

AUTH_USER_MODEL = 'geba_auth.User'

WSGI_APPLICATION = 'config.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

SUMMERNOTE_THEME = 'bs4'  # Show summernote with Bootstrap4

FORCE_SESSION_TO_ONE = False
FORCE_INACTIVE_USER_END_SESSION = True

# ---- tinymce settings ---------

TINYMCE_DEFAULT_CONFIG = {
    'height': 360,
    'width': 1120,
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'theme': 'modern',
    'browser_spellcheck': True,
    'plugins': '''
            textcolor save link image media preview codesample contextmenu
            table code lists fullscreen  insertdatetime  nonbreaking
            contextmenu directionality searchreplace wordcount visualblocks
            visualchars code fullscreen autolink lists  charmap print  hr
            anchor pagebreak toc
            ''',
    'toolbar1': '''
            fullscreen preview bold italic underline | fontselect,
            fontsizeselect  | forecolor backcolor | alignleft alignright |
            aligncenter alignjustify | indent outdent | bullist numlist table |
            | link image media | codesample |
            ''',
    'toolbar2': '''
            visualblocks visualchars |
            charmap hr pagebreak nonbreaking anchor |  code |
            ''',
    'contextmenu': 'formats | link image',
    'menubar': True,
    'statusbar': True,
    # 'images_reuse_filename': True,
    # 'images_upload_url': True,
}

TINYMCE_ADDITIONAL_JS_URLS = {
    'apps/core/js/filebrowser_s3.js',
}

TINYMCE_CALLBACKS = {
    # 'file_browser_callback': 'myFileBrowser',
    # 'images_upload_handler': 'customHandler',
    'file_picker_callback': 'customFilePicker',
}

TINYMCE_FILEBROWSER = True

FILEBROWSER_DIRECTORY = ''
DIRECTORY = ''
