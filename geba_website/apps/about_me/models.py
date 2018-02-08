from django.db import models

# Create your models here.


class AboutMe(models.Model):

    photo = models.FileField()
    content = models.TextField()

