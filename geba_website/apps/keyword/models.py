from django.db import models
# Create your models here.


def upload_location(instance, filename):
    """returns the location of where to save the post images"""
    return "keyword/%s/%s" % (instance.slug, filename)


class Keyword(models.Model):

    slug = models.SlugField(unique=True)

    keyword = models.CharField(max_length=200)

    image = models.ImageField(upload_to=upload_location,
                              null=True,
                              blank=True,
                              width_field="width_field",
                              height_field="height_field")

    width_field = models.IntegerField(default=0, null=True)
    height_field = models.IntegerField(default=0, null=True)

    def __str__(self):
        return self.keyword
