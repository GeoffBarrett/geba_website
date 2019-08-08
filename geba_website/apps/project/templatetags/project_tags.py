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


@register.filter()
def get_adj_slug(objs, superuser):
    """
    This will be used for the get next and previous projects functionality. Since we reverse the order list in the
    model's get_prev_slug, the same filter should work both operations
    """
    if not superuser:
        # if you are superuser return all the related objects
        objs = objs.filter(draft=False, publish_date__lte=timezone.now())

    if objs:
        return objs[0].slug
    else:
        return None


@register.filter()
def active_project(obj, superuser):

    if not superuser:

        if  obj.draft and obj.publish_date <= timezone.now():
            return None

    return obj.slug