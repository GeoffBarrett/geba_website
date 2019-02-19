import os
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import pre_save, pre_delete, post_save  # before saving it emits this signal
from django.utils.text import slugify  # turns our title into a slug
from ..core.models import TimeStampModel
from django.utils.safestring import mark_safe
# from markdown_deux import markdown
from ..comments.models import Comment
from ..vote.models import VoteModel
from ..keyword.models import Keyword
from django.contrib.contenttypes.models import ContentType
# from django.db import transaction
# from tinymce.widgets import TinyMCE
# from datetime import datetime
from django.db.models import Q


def upload_location(instance, filename):
    """returns the location of where to save the post images"""
    return "blog/%s/%s" % (instance.slug, filename)


class PostManager(models.Manager):

    def search(self, query=None):
        """This will search based off of the query"""
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(title__icontains=query) |
                         Q(body__icontains=query) |
                         Q(slug__icontains=query)
                         )
            qs = qs.filter(or_lookup).distinct()  # distinct() is often necessary with Q lookups
        return qs

    def active(self, *args, **kwargs):
        """overwriting Post.objects.all()"""
        return super(PostManager, self).filter(draft=False, publish_date__lte=timezone.now())

    def latest(self, *args, **kwargs):
        """overwriting Post.objects.all()"""
        try:
            return super(PostManager, self).filter(draft=False, publish_date__lte=timezone.now())[0]
        except IndexError:
            return []


class Post(VoteModel, TimeStampModel):

    score_method = 'hot_score'

    objects = PostManager()

    slug = models.SlugField(unique=True)

    publish_date = models.DateTimeField(blank=True, null=True, default=timezone.now())

    title = models.CharField(max_length=200)

    image = models.ImageField(upload_to=upload_location,
                              null=True,
                              blank=True,
                              width_field="width_field",
                              height_field="height_field")

    width_field = models.IntegerField(default=0, null=True)
    height_field = models.IntegerField(default=0, null=True)

    image_caption = models.CharField(blank=True, null=True, max_length=200)

    draft = models.BooleanField(default=False)

    body = models.TextField()

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    # author = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    # keywords = models.TextField(blank=True, null=True)
    keywords = models.ManyToManyField(Keyword, blank=True)

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})

    def __str__(self):  # when calling Posts.title we want to make sure it returns a string instead of a Posts object
        return self.title

    class Meta:
        ordering = ["-vote_score", "-num_vote_up", "-publish_date", "-modified"]

    def get_delete_url(self):
        return reverse("blog:delete", kwargs={"slug": self.slug})

    def get_html(self):
        """converts the body to markdown so we don\'t have to use the |markdown filter"""
        body = self.body
        return mark_safe(body)

    def get_api_like_url(self):
        return reverse("blog:like_toggle_api", kwargs={'slug': self.slug})

    def get_api_dislike_url(self):
        return reverse("blog:dislike_toggle_api", kwargs={'slug': self.slug})

    @property
    def comments(self):
        """creating a method to allow the post form to grab the post comments"""
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


def create_slug(instance, new_slug=None):
    """Appends an id at the end of the slug, if the slug is found"""
    slug = slugify(instance.title)  # create a slug of the file
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def has_image(instance):

    if instance.image == '':
        return False
    elif instance.image is None:
        return False

    return True


def pre_save_post_signal_receiver(sender, instance, *args, **kwargs):
    """This signal is sent at the beginning of the save() method,
    sender = models class,
    instance = instance being saved,
    """
    if not instance.slug:
        # if there is no slug, create one
        instance.slug = create_slug(instance=instance)
    else:
        # then the post already exists
        post_instance = Post.objects.filter(pk=instance.pk)[0]

        if has_image(instance) and has_image(post_instance):
            if post_instance.image.url != instance.image.url:
                # then we can delete the old image

                delete_image(post_instance)

        elif not has_image(instance) and has_image(post_instance):
            # then you have removed the old image
            delete_image(post_instance)


'''
def post_save_post_signal_receiver(sender, instance, *args, **kwargs):
    """This signal is sent at the after the save() method,
    sender = models class,
    instance = instance being saved,
    """

    if kwargs['created']:
        instance.votes.up(instance.author.id)
'''


def pre_delete_post_signal_receiver(sender, instance, *args, **kwargs):
    """This will ensure to modify the authors ManytoManyField if necessary and delete an author if
    there are no more posts in the project with that authors name."""

    # delete the comments on the project post
    comments = instance.comments
    for comment in comments:
        comment.delete()

    # delete image of the project post
    delete_image(instance)


def delete_image(instance):
    if instance.image:
        # if an image exists, delete it
        try:
            # this only really works locally when it accepts fullpaths
            img_path = instance.image.path

            if os.path.isfile(img_path):
                img_dir = os.path.dirname(img_path)
                os.remove(img_path)

                if len(os.listdir(img_dir)) == 0:
                    # if the directory that the image is in is empty, delete it
                    os.rmdir(img_dir)
        except NotImplementedError:
            # you have to use the delete function to properly do it with S3, probably can just do this from the
            # beginning
            instance.image.delete(save=False)


pre_save.connect(pre_save_post_signal_receiver, sender=Post)  # connects the signal with the signal receiver
pre_delete.connect(pre_delete_post_signal_receiver, sender=Post)  # connects the signal with the signal receiver

# post_save.connect(post_save_post_signal_receiver, sender=Post)  # connects the signal with the signal receiver
