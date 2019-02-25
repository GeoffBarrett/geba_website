# custom_storages.py
# from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
# from filebrowser.storage import StorageMixin
from filebrowser_safe.storage import StorageMixin
'''
class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION

    def _clean_name(self, name):
        return name

    def _normalize_name(self, name):
        if name[0] == '/':
            name = name[1:]

        # name += self.location # this puts /static at the end
        name = '%s/%s' % (self.location, name)
        return name


class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION

    def _clean_name(self, name):
        return name

    def _normalize_name(self, name):
        if name[0] == '/':
            name = name[1:]

        # name += self.location # this puts /static at the end
        name = '%s/%s' % (self.location, name)
        return name
'''

# StaticStorage = lambda: S3Boto3Storage(location='static')


class StaticStorage(StorageMixin, S3Boto3Storage):
    location = 'static'

# MediaStorage = lambda: S3Boto3Storage(location='media')


class MediaStorage(StorageMixin, S3Boto3Storage):
    location = 'media'
