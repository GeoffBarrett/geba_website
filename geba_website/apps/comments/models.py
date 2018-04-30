from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from ..vote.models import VoteModel
# Create your models here.


class CommentManager(models.Manager):
    def all(self):
        return super(CommentManager, self).filter(parent=None)

    def filter_by_instance(self, instance):
        # instance.__class__ ensures that it works for a multitude of object types / models
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        return super(CommentManager, self).filter(content_type=content_type, object_id=obj_id).filter(parent=None)


class Comment(VoteModel, models.Model):

    score_method = 'confidence'

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # the model that the comment is associated with
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()  # the id of the object with that model that the comment was on
    content_object = GenericForeignKey('content_type', 'object_id')  # the comment object
    # content_object = GenericForeignKey()  # the object that was voted on

    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CommentManager()

    class Meta:
        ordering = ["-vote_score", "-num_vote_up", "-timestamp"]  # order by newest comments

    def __str__(self):
        return str(self.author.username)

    def children(self, user_id):
        qs = Comment.objects.filter(parent=self)
        return Comment.votes.annotate(queryset=qs, user_id=user_id)

    @property
    def is_parent(self):
        if self.parent is not None:
            # if it returns a parent then it isn't a parent
            return False
        return True

    def get_absolute_url(self):
        return reverse("comments:thread", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("comments:delete", kwargs={"pk": self.pk})

    def get_api_like_url(self):
        return reverse("comments:like_toggle_api", kwargs={'pk': self.pk})

    def get_api_dislike_url(self):
        return reverse("comments:dislike_toggle_api", kwargs={'pk': self.pk})



