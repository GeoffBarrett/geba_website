from django.db import models
from ..core.models import TimeStampModel
from django.urls import reverse
from django.utils.safestring import mark_safe
import os
from django.db.models.signals import pre_save, pre_delete  # before saving it emits this signal


def upload_location(instance, filename):
    """returns the location of where to save the post images"""
    return "pages/%s/%s" % (instance.slug, filename)


class Page(TimeStampModel):

    # objects = PostManager()

    slug = models.SlugField(unique=True)

    title = models.CharField(max_length=200)
    show_title = models.BooleanField(default=True)

    header_image = models.ImageField(upload_to=upload_location,
                                     null=True,
                                     blank=True,
                                     width_field="width_field",
                                     height_field="height_field")

    width_field = models.IntegerField(default=0, null=True)
    height_field = models.IntegerField(default=0, null=True)

    body = models.TextField()

    def get_absolute_url(self):
        return reverse('pages:detail', kwargs={'slug': self.slug})

    def __str__(self):  # when calling Posts.title we want to make sure it returns a string instead of a Posts object
        return self.title

    def get_delete_url(self):
        return reverse("pages:delete", kwargs={"slug": self.slug})

    def get_html(self):
        """converts the body to markdown so we don't have to use the |markdown filter"""
        body = self.body
        return mark_safe(body)


def delete_image(instance):
    if instance.header_image:
        # if an image exists, delete it
        try:
            # this only really works locally when it accepts fullpaths
            img_path = instance.header_image.path

            if os.path.isfile(img_path):
                img_dir = os.path.dirname(img_path)
                os.remove(img_path)

                if len(os.listdir(img_dir)) == 0:
                    # if the directory that the image is in is empty, delete it
                    os.rmdir(img_dir)
        except NotImplementedError:
            # you have to use the delete function to properly do it with S3, probably can just do this from the
            # beginning
            instance.header_image.delete(save=False)


def pre_delete_page_signal_receiver(sender, instance, *args, **kwargs):
    """This will ensure to modify the authors ManytoManyField if necessary and delete an author if
    there are no more posts in the project with that authors name."""

    # delete image of the page
    delete_image(instance)


pre_delete.connect(pre_delete_page_signal_receiver, sender=Page)  # connects the signal with the signal receiver
