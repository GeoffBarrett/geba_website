# custom_storages.py
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage, S3Boto3StorageFile
from django.utils.timezone import localtime
from filebrowser.storage import StorageMixin
import datetime
# from filebrowser_safe.storage import StorageMixin

StaticStorageLocal = lambda: S3Boto3Storage(location='static')
MediaStorageLocal = lambda: S3Boto3Storage(location='media')

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

''''''


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

    def isdir(self, name):
        if not name:  # Empty name is a directory
            return True

        if self.isfile(name):
            return False

        for item in super(StaticStorage, self).listdir(name):
            if len(item):
                return True

        return False

    def isfile(self, name):
        try:
            name = self._normalize_name(self._clean_name(name))
            f = S3Boto3StorageFile(name, 'rb', self)
            if "directory" in f.obj.content_type:
                return False
            return True
        except Exception:
            return False

    def makedirs(self, name):
        name = self._normalize_name(self._clean_name(name))
        return self.bucket.meta.client.put_object(Bucket=self.bucket.name, Key=f'{name}/')

    def rmtree(self, name):
        name = self._normalize_name(self._clean_name(name))
        delete_objects = [{'Key': f"{name}/"}]

        dirlist = self.listdir(self._encode_name(name))
        for item in dirlist:
            for obj in item:
                obj_name = f"{name}/{obj}"
                if self.isdir(obj_name):
                    obj_name = f"{obj_name}/"
                delete_objects.append({'Key': obj_name})
        self.bucket.delete_objects(Delete={'Objects': delete_objects})

    def path(self, name):
        return name

    def listdir(self, name):
        directories, files = super().listdir(name)
        if '.' in files:
            files.remove('.')
        return directories, files

    def exists(self, name):
        if self.isdir(name):
            return True
        else:
            return super().exists(name)

    def get_modified_time(self, name):
        # S3 boto3 library requires that directories have the trailing slash
        if self.isdir(name):
            name = f'{name}/'
        return super().get_modified_time(name)

    def size(self, name):
        # S3 boto3 library requires that directories have the trailing slash
        if self.isdir(name):
            name = f'{name}/'
        return super().size(name)


class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION

    def isdir(self, name):
        if not name:  # Empty name is a directory
            return True
        if self.isfile(name):
            return False

        for item in super(MediaStorage, self).listdir(name):
            if len(item):
                return True
        return False

    def isfile(self, name):
        try:
            name = self._normalize_name(self._clean_name(name))
            f = S3Boto3StorageFile(name, 'rb', self)
            if "directory" in f.obj.content_type:
                return False
            return True
        except Exception:
            return False

    def makedirs(self, name):
        name = self._normalize_name(self._clean_name(name))
        return self.bucket.meta.client.put_object(Bucket=self.bucket.name, Key=f'{name}/')

    def rmtree(self, name):
        name = self._normalize_name(self._clean_name(name))
        delete_objects = [{'Key': f"{name}/"}]

        dirlist = self.listdir(self._encode_name(name))
        for item in dirlist:
           for obj in item:
                obj_name = f"{name}/{obj}"
                if self.isdir(obj_name):
                    obj_name = f"{obj_name}/"
                delete_objects.append({'Key': obj_name})
        self.bucket.delete_objects(Delete={'Objects': delete_objects})

    def path(self, name):
        return name

    def listdir(self, name):
        directories, files = super().listdir(name)
        if '.' in files:
            files.remove('.')
        return directories, files

    def exists(self, name):
        if self.isdir(name):
            return True
        else:
            return super().exists(name)

    def get_modified_time(self, name):
        # S3 boto3 library requires that directories have the trailing slash

        dirBool = False
        if self.isdir(name):
            name = f'{name}/'
            dirBool = True

        name = self._normalize_name(self._clean_name(name))
        entry = self.entries.get(name)

        # only call self.bucket.Object() if the key is not found
        # in the preloaded metadata.
        if entry is None:
            entry = self.bucket.Object(self._encode_name(name))

        if settings.USE_TZ:
            # boto3 returns TZ aware timestamps
            if dirBool:
                mod_time = datetime.datetime.now()
            else:
                mod_time = entry.last_modified

            return mod_time
        else:
            if dirBool:
                mod_time = localtime(datetime.datetime.now()).replace(tzinfo=None)
            else:
                mod_time = localtime(entry.last_modified).replace(tzinfo=None)

            return mod_time

    def size(self, name):
        # S3 boto3 library requires that directories have the trailing slash

        dir = False
        if self.isdir(name):
            name = f'{name}/'
            dir = True

        if not dir:
            return super().size(name)
        else:
            return 0


