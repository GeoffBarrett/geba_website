from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Create your models here.
from .signals import object_viewed_signal
from .utils import get_client_ip
from django.db.models.signals import post_save
from django.contrib.sessions.models import Session
from ..geba_auth.signals import user_logged_in
from django.utils import timezone
from calendar import monthrange


tz = getattr(settings, 'TIME_ZONE', 'UTC')

FORCE_SESSION_TO_ONE = getattr(settings, 'FORCE_SESSION_TO_ONE', False)
FORCE_INACTIVE_USER_END_SESSION = getattr(settings, 'FORCE_INACTIVE_USER_END_SESSION', False)


class ObjectViewedManager(models.Manager):
    def today(self, *args, **kwargs):
        """overwriting Post.objects.all()"""
        viewed_today = super(ObjectViewedManager, self).filter(timestamp__gte=timezone.now().replace(
            hour=0, minute=0, second=0), timestamp__lte=timezone.now().replace(hour=23, minute=59, second=59))

        anonymous_views = viewed_today.filter(user=None).count()

        return viewed_today.count() - anonymous_views, anonymous_views

    def daily(self, *args, **kwargs):
        """overwriting Post.objects.all()"""

        current_month = timezone.now().month
        current_year = timezone.now().year
        current_day = timezone.now().day

        daily_labels = []
        daily_data = []
        daily_anonymous_data = []

        for i in range(1, current_day+1):
            date_string = '%d-%02d-%02d' % (current_year, current_month, i)
            start_time = timezone.datetime.strptime(date_string, "%Y-%m-%d")  # # Expects "YYYY-MM-DD" string
            stop_time = timezone.datetime.strptime(date_string, "%Y-%m-%d").replace(hour=23, minute=59, second=59)

            daily_qs = super(ObjectViewedManager, self).filter(timestamp__gte=start_time, timestamp__lte=stop_time)

            anon_count = daily_qs.filter(user=None).count()

            daily_data.append(daily_qs.count()-anon_count)
            daily_anonymous_data.append(anon_count)
            daily_labels.append(i)

        return daily_labels, daily_data, daily_anonymous_data

    def monthly(self, *args, **kwargs):
        """overwriting Post.objects.all()"""

        current_month = timezone.now().month
        current_year = timezone.now().year

        monthly_views = []
        monthly_anonymous_views = []
        monthly_views_labels = []

        for i in range(current_month):
            date_string = '%d-%02d-%02d' % (current_year, i+1, 1)
            start_time = timezone.datetime.strptime(date_string, "%Y-%m-%d")  # # Expects "YYYY-MM-DD" string

            last_of_month = monthrange(current_year, i + 1)[-1]
            date_string = '%d-%02d-%02d' % (current_year, i + 1, last_of_month)
            stop_time = timezone.datetime.strptime(date_string, "%Y-%m-%d").replace(hour=23, minute=59, second=59)

            monthly_qs = super(ObjectViewedManager, self).filter(timestamp__gte=start_time, timestamp__lte=stop_time)

            anon_count = monthly_qs.filter(user=None).count()

            monthly_views.append(monthly_qs.count() - anon_count)
            monthly_anonymous_views.append(anon_count)
            monthly_views_labels.append(start_time.strftime('%B'))

        return monthly_views_labels, monthly_views, monthly_anonymous_views

    def yearly(self, *args, **kwargs):
        """overwriting Post.objects.all()"""
        current_year = timezone.now().year


class ObjectViewed(models.Model):
    """
    This model will record details about other models that have been viewed so we can collect analytics on this
    information.

    """

    objects = ObjectViewedManager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)
    ip_address = models.CharField(max_length=120, blank=True, null=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self, ):
        # return "%s viewed: %s" % (self.content_object, self.timestamp)
        return "%s viewed" % self.content_object

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Object Viewed'
        verbose_name_plural = 'Objects Viewed'


def object_viewed_receiver(sender, instance, request, *args, **kwargs):
    """
    This is a receiver that the signal will connect to whenever a user views an object. Essentially whenever a DetailView
    that we place a specific mixin is accessed, this receiver will create an ObjectViewed instance saying what was viewed,
    who viewed it, the IP of the viewer, etc.

    :param sender: the object type that is being viewed sent this signal.
    :param instance: the instance of the object type
    :param request: the request that is being made
    :param args:
    :param kwargs:
    :return:
    """
    c_type = ContentType.objects.get_for_model(sender)

    # have to take in account if the user is not signed in.
    if request.user.is_anonymous:
        user = None
    else:
        user = request.user

    new_view_obj = ObjectViewed.objects.create(user=user,
                                               ip_address=get_client_ip(request),
                                               object_id=instance.id,
                                               content_type=c_type
                                               )


object_viewed_signal.connect(object_viewed_receiver)


class UserSession(models.Model):
    """
    This model will contain information about a user's session whenever a user logs on the website.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)
    ip_address = models.CharField(max_length=120, blank=True, null=True)
    session_key = models.CharField(max_length=100, blank=True, null=True)  # grab a user's session key
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)  # if the session is active
    ended = models.BooleanField(default=False)  # if we want to end a session

    def end_session(self):
        session_key = self.session_key
        # ended = self.ended
        try:
            Session.objects.get(pk=session_key).delete()
            self.active = False
            self.ended = True
            self.save()
        except:
            pass
        return self.ended


def post_save_session_receiver(sender, instance, created, *args, **kwargs):
    # ends all other sessions besides the created one
    if created:
        qs = UserSession.objects.filter(user=instance.user, ended=False, active=False).exclude(id=instance.id)
        for i in qs:
            i.end_sessions()

    # makes it so you can end sessions in the admin
    if not instance.active and not instance.ended:
        instance.end_session()


def post_save_user_changed_receiver(sender, instance, created, *args, **kwargs):
    """This will end all users sessions if it wasn't just created"""
    if not created:
        if instance.is_active is False:
            qs = UserSession.objects.filter(user=instance.user, ended=False, active=False)
            for i in qs:
                i.end_sessions()


if FORCE_INACTIVE_USER_END_SESSION:
    post_save.connect(post_save_user_changed_receiver, sender=UserSession)

if FORCE_SESSION_TO_ONE:
    post_save.connect(post_save_session_receiver, sender=UserSession)


def user_logged_in_receiver(sender, instance, request, *args, **kwargs):
    user = instance
    ip_address = get_client_ip(request)
    session_key = request.session.session_key

    UserSession.objects.create(
        user=user,
        ip_address=ip_address,
        session_key=session_key
    )


user_logged_in.connect(user_logged_in_receiver)
