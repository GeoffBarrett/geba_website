from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
# Create your models here.
from ..core.models import TimeStampModel


def upload_location(instance, filename):
    """returns the location of where to save the post images"""
    return "%s/%s" % (instance.id, filename)


def Page(TimeStampModel):

    slug = models.SlugField(unique=True)

    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)

    image = models.ImageField(upload_to=upload_location,
                              null=True,
                              blank=True,
                              width_field="width_field",
                              height_field="height_field")

    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)

    image_caption = models.CharField(blank=True, null=True, max_length=200)

    body = models.TextField()

    draft_body = models.TextField(blank=True, null=True)

    last_edited_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})

    def __str__(self):  # when calling Posts.title we want to make sure it returns a string instead of a Posts object
        return self.title

    class Meta:
        ordering = ["-publish_date", "-modified"]