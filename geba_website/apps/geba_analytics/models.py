from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Create your models here.
from .signals import object_viewed_signal
from .utils import get_client_ip


class ObjectViewed(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)
    ip_address = models.CharField(max_length=120, blank=True, null=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self, ):
        return "%s viewed: %s" % (self.content_object, self.timestamp)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Object Viewed'
        verbose_name_plural = 'Objects Viewed'


def object_viewed_receiver(sender, instance, request, *args, **kwargs):

    print('hiiiiii')
    c_type = ContentType.objects.get_for_model(sender)
    new_view_obj = ObjectViewed.objects.create(user=request.user,
                                               ip_address=get_client_ip(request),
                                               object_id=instance.id,
                                               content_type=c_type
                                               )


object_viewed_signal.connect(object_viewed_receiver)
