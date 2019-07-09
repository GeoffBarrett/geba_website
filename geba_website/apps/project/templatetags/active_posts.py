# core.templatetags.class_name.py
from django import template
from django.utils import timezone

register = template.Library()


@register.filter()
def active_posts(objs, superuser):
    """
    This filter makes it so the draft / unpublished project posts do not get shown to those that are not superusers
    """
    if superuser:
        # if you are superuser return all the related objects
        return objs

    # if not, then you make sure to only show the published posts.
    return objs.filter(draft=False, publish_date__lte=timezone.now())
