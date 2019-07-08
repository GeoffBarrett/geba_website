# core.templatetags.class_name.py
from django import template
from django.utils import timezone

register = template.Library()


@register.filter()
def active_posts(objs, superuser):

    print('superuser------', superuser)
    if superuser:
        return objs

    return objs.filter(draft=False, publish_date__lte=timezone.now())
