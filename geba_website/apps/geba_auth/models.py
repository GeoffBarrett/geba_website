from django.db import models
from django.contrib.auth.models import AbstractUser


def upload_location(instance, filename):
    """returns the location of where to save the post images"""
    return "%s/%s" % (instance.username, filename)


class User(AbstractUser):

    bio = models.TextField(max_length=500, blank=True)

    avatar = models.ImageField(upload_to=upload_location,
                               null=True,
                               blank=True,
                               width_field="width_field",
                               height_field="height_field")

    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)

