from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import pre_save, pre_delete, post_save  # before saving it emits this signal
from ..core.models import TimeStampModel
from django.utils.safestring import mark_safe
# from markdown_deux import markdown
from ..comments.models import Comment
from ..vote.models import VoteModel
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# from tinymce.models import HTMLField
# from django.shortcuts import get_object_or_404
# from django.db import transaction
import os
from django.utils.text import slugify  # turns our title into a slug

# Create your models here.


def upload_location(instance, filename):
    """returns the location of where to save the post images"""
    return "projects/%s/%s" % (instance.slug, filename)


class ProjectPostManager(models.Manager):
    def active(self, *args, **kwargs):
        """overwriting Post.objects.all()"""
        return super(ProjectPostManager, self).filter(draft=False, publish_date__lte=timezone.now())

    def latest(self, *args, **kwargs):
        try:
            return super(ProjectPostManager, self).filter(draft=False, publish_date__lte=timezone.now())[0]
        except IndexError:
            return []


class ProjectManager(models.Manager):
    def active(self, *args, **kwargs):
        """overwriting Post.objects.all()"""
        # return super(ProjectManager, self).filter(draft=False).filter(publish_date__lte=timezone.now())
        return super(ProjectManager, self).filter(draft=False, publish_date__lte=timezone.now(),
                                                  authors__isnull=False).exclude(body__exact='')

    def latest(self, *args, **kwargs):
        try:
            return super(ProjectManager, self).filter(draft=False, publish_date__lte=timezone.now(),
                                                      authors__isnull=False).exclude(body__exact='')[0]
        except IndexError:
            return []


class ProjectPost(VoteModel, TimeStampModel):

    score_method = 'hot_score'

    objects = ProjectPostManager()

    post_order = models.IntegerField(null=True, blank=True)

    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE)  # the model that the parent is associated with

    object_id = models.PositiveIntegerField()  # the id of the object with that model that the project belongs to
    content_object = GenericForeignKey('content_type', 'object_id')  # the project object
    # parent = models.ForeignKey('self', null=True, blank=True)

    slug = models.SlugField(unique=True)

    publish_date = models.DateTimeField(blank=True, null=True)

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

    keywords = models.TextField(blank=True, null=True)

    def get_project_posts(self):
        """This method will be used in post_detail.html to have a list of related posts"""
        return ProjectPost.objects.filter(object_id=self.object_id)

    def get_next_post_order(self):
        """This method will return the post order when a new post is being created, it will default as the
        immediate next post"""
        return int(len(ProjectPost.objects.filter(object_id=self.object_id)) + 1)

    def get_project_slug(self):
        return Project.objects.filter(id=self.object_id)[0].slug

    def get_project(self):
        return Project.objects.filter(id=self.object_id)[0]

    def get_absolute_url(self):
        return reverse('project:detail', kwargs={'slug': self.slug})

    def get_api_like_url(self):
        return reverse("project:post_like_toggle_api", kwargs={'slug': self.slug})

    def get_api_dislike_url(self):
        return reverse("project:post_dislike_toggle_api", kwargs={'slug': self.slug})

    def __str__(self):  # when calling Posts.title we want to make sure it returns a string instead of a Posts object
        return self.title

    class Meta:
        ordering = ["post_order", "-num_vote_up", "-publish_date", "-modified"]

    def get_html(self):
        '''converts the body to markdown so we don\'t have to use the |markdown filter'''
        body = self.body
        # return mark_safe(markdown(body))
        return mark_safe(body)

    @property
    def comments(self):
        '''creating a method to allow the post form to grab the post comments'''
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

    @property
    def is_future_publication(self):
        return self.publish_date > timezone.now()


class Project(VoteModel, TimeStampModel):
    """This model will contain attributes related to Projects"""

    # this is the individual that created the
    # author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    # list of all the authors for this project, could make this a property... probably should.
    authors = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    body = models.TextField(blank=True, null=True)

    score_method = 'hot_score'

    objects = ProjectManager()

    slug = models.SlugField(unique=True)

    publish_date = models.DateTimeField(blank=True, null=True)

    title = models.CharField(max_length=200)
    pages = models.ManyToManyField(ProjectPost, blank=True)

    image = models.ImageField(upload_to=upload_location,
                              null=True,
                              blank=True,
                              width_field="width_field",
                              height_field="height_field")

    width_field = models.IntegerField(default=0, null=True)
    height_field = models.IntegerField(default=0, null=True)

    image_caption = models.CharField(blank=True, null=True, max_length=200)

    draft = models.BooleanField(default=False)

    keywords = models.TextField(blank=True, null=True)

    def get_html(self):
        '''converts the body to markdown so we don\'t have to use the |markdown filter'''
        body = self.body
        # return mark_safe(markdown(body))
        return mark_safe(body)

    def get_delete_url(self):
        return reverse("project:delete", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["-vote_score", "-num_vote_up", "-publish_date", "-modified"]

    def get_absolute_url(self):

        if self.body == '':
            # object = get_object_or_404(Project, slug=self.slug)
            object = Project.objects.filter(slug=self.slug)

            # posts = get_object_or_404(ProjectPost, object_id=object[0].id)
            posts = ProjectPost.objects.filter(object_id=object[0].id)
            if len(posts) == 0:
                # returns the same url if the project has no ProjectPosts
                return '#'
            else:
                # return the first page in the project
                return reverse('project:detail', kwargs={'slug': posts[0].slug})
        else:
            return reverse('project:detail', kwargs={'slug': self.slug})

    def get_description(self):
        if self.body == '':
            object = Project.objects.filter(slug=self.slug)
            posts = ProjectPost.objects.filter(object_id=object[0].id)
            content = posts[0].body

            return content
        else:
            return self.body

    def get_api_like_url(self):
        return reverse("project:project_like_toggle_api", kwargs={'slug': self.slug})

    def get_api_dislike_url(self):
        return reverse("project:project_dislike_toggle_api", kwargs={'slug': self.slug})

    def get_project_posts(self):
        """This method will be used in post_detail.html to have a list of related posts"""
        return ProjectPost.objects.filter(object_id=self.id)

    def get_next_post_order(self):
        """This method will return the post order when a new post is being created, it will default as the
        immediate next post"""
        return int(len(ProjectPost.objects.filter(object_id=self.id)) + 1)

    '''
    @property
    def authors(self):
        """This is if I decide that I want to convert the authors list into a property instead of a model field"""
        authors = [post.author for post in self.pages.all()]
        return list(set(authors + [self.author]))
    '''

    @property
    def comments(self):
        '''creating a method to allow the post form to grab the post comments'''
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

    @property
    def is_future_publication(self):
        return self.publish_date > timezone.now()


def create_slug(instance, prepend_slug=None, new_slug=None):
    """
    Appends an id at the end of the slug, if the slug is found
    this will check if the slug exists for the project slug or the project post slug, making sure that they both
    don't have the same slug.
    """

    slug = slugify(instance.title)  # create a slug of the file
    if new_slug is not None:
        slug = new_slug

    if prepend_slug is not None:
        # if the model is a project post, we will prepend the project slug to the beginning
        slug = '%s-%s' % (prepend_slug, slug)

    qs = ProjectPost.objects.filter(slug=slug).order_by("-id")
    qs2 = Project.objects.filter(slug=slug).order_by("-id")

    exists = qs.exists()
    exists2 = qs2.exists()
    if exists or exists2:
        if exists:
            new_slug = "%s-%s" % (slug, qs.first().id)
        elif exists2:
            new_slug = "%s-%s" % (slug, qs2.first().id)
        return create_slug(instance, prepend_slug=prepend_slug, new_slug=new_slug)
    return slug


def has_image(instance):

    if instance.image == '':
        return False
    elif instance.image is None:
        return False

    return True


def pre_save_project_signal_receiver(sender, instance, *args, **kwargs):
    """This signal is sent at the beginning of the save() method,
    sender = models class,
    instance = instance being saved,
    """
    if not instance.slug:
        # if there is no slug, create one
        instance.slug = create_slug(instance=instance)
    else:
        # then the project already exists
        project_instance = Project.objects.filter(pk=instance.pk)[0]

        if has_image(instance) and has_image(project_instance):
            if project_instance.image.url != instance.image.url:
                # then we can delete the old image

                delete_image(project_instance)

        elif not has_image(instance) and has_image(project_instance):
            # then you have removed the old image
            delete_image(project_instance)


def pre_save_signal_projectpost_receiver(sender, instance, *args, **kwargs):
    """This signal is sent at the beginning of the save() method,
    sender = models class,
    instance = instance being saved,
    """
    if not instance.slug:

        project_instance = Project.objects.filter(id=instance.object_id)[0]

        # if there is no slug, create one
        instance.slug = create_slug(instance=instance, prepend_slug=project_instance.slug)
    else:
        # then the projectpost already exists
        post_instance = ProjectPost.objects.filter(pk=instance.pk)[0]

        if has_image(instance) and has_image(post_instance):
            if post_instance.image.url != instance.image.url:
                # then we can delete the old image
                delete_image(post_instance)

        elif not has_image(instance) and has_image(post_instance):
            # then you have removed the old image
            delete_image(post_instance)


def pre_delete_projectpost_signal_receiver(sender, instance, *args, **kwargs):
    """This will ensure to modify the authors ManytoManyField if necessary and delete an author if
    there are no more posts in the project with that authors name."""

    try:
        project_instance = Project.objects.filter(id=instance.object_id)[0]
    except IndexError:
        # if the project instance was already deleted, you will get an instance error
        return

    # get the authors of the posts (excluding the current instance
    authors = [post.author for post in project_instance.pages.all() if post != instance]

    if instance.author not in authors:
        project_instance.authors.remove(instance.author)
        project_instance.save()

    # delete the comments on the project post
    comments = instance.comments
    for comment in comments:
        comment.delete()

    # delete image of the project post
    delete_image(instance)


def pre_delete_project_signal_receiver(sender, instance, *args, **kwargs):
    """This will be used to delete the project posts that go along with the project"""

    project_posts = instance.get_project_posts()

    for post in project_posts:
        post.delete()

    # delete the image of the project
    delete_image(instance)


def delete_image(instance):
    if instance.image:
        # if an image exists, delete it
        img_path = instance.image.path

        if os.path.isfile(img_path):
            img_dir = os.path.dirname(img_path)
            os.remove(img_path)
            if len(os.listdir(img_dir)) == 0:
                # if the directory that the image is in is empty, delete it
                os.rmdir(img_dir)


# connects the signal with the signal receiver
pre_save.connect(pre_save_signal_projectpost_receiver, sender=ProjectPost)
pre_save.connect(pre_save_project_signal_receiver, sender=Project)  # connects the signal with the signal receiver

pre_delete.connect(pre_delete_projectpost_signal_receiver, sender=ProjectPost)
pre_delete.connect(pre_delete_project_signal_receiver, sender=Project)
