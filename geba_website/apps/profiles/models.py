from django.db import models
from django.conf import settings

from django.utils.translation import ugettext_lazy as _
# Create your models here.




class DefaultProfile(models.Model):
    """The default user profile"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
