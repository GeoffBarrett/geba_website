from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class TimeStampModel(models.Model):
    """model class for updating modified/created fields
    We will probably use a created/modified field for everything
    so might as well create a class to do it for us

    abstract base class: tables are only created for derived models"""

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ModelFormFailureHistory(models.Model):
    form_data = models.TextField()
    model_data = models.TextField()


class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)

