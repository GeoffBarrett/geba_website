from django.db import models
from ..comments.models import Comment
from ..vote.models import VoteModel
from ..core.models import TimeStampModel
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
# Create your models here.


class ForumManager(models.Manager):
    def active(self, *args, **kwargs):
        """overwriting Post.objects.all()"""
        return super(ForumManager, self).filter(draft=False, publish_date__lte=timezone.now())

    def latest(self, *args, **kwargs):
        """overwriting Post.objects.all()"""
        try:
            return super(ForumManager, self).filter(draft=False, publish_date__lte=timezone.now())[0]
        except IndexError:
            return []


class ForumPost(VoteModel, TimeStampModel):

    objects = ForumManager()

    score_method = 'hot_score'

    slug = models.SlugField(unique=True)

    publish_date = models.DateTimeField(blank=True, null=True)

    title = models.CharField(max_length=200)

    draft = models.BooleanField(default=False)

    body = models.TextField()

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    # author = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    def __str__(self):  # when calling Posts.title we want to make sure it returns a string instead of a Posts object
        return self.title

    class Meta:
        ordering = ["-vote_score", "-num_vote_up", "-publish_date", "-modified"]

    @property
    def comments(self):
        '''creating a method to allow the post form to grab the post comments'''
        instance = self
        return Comment.objects.filter_by_instance(instance)

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

    @property
    def is_future_publication(self):
        return self.publish_date > timezone.now()