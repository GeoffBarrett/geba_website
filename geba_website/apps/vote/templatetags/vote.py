from __future__ import absolute_import

from django import template
from django.contrib.auth.models import AnonymousUser

from ..models import UP, DOWN

register = template.Library()


@register.simple_tag
def vote_exists(model, user=AnonymousUser()):
    if user.is_anonymous():
        return False
    if model.votes.exists(user.pk, action=UP):
        return "UP"
    elif model.votes.exists(user.pk, action=DOWN):
        return "DOWN"
    else:
        return False

'''
@register.filter
def vote_exists(model, geba_auth=AnonymousUser()):
    if geba_auth.is_anonymous():
        return False
    if model.votes.exists(geba_auth.pk, action=UP):
        return "UP"
    elif model.votes.exists(geba_auth.pk, action=DOWN):
        return "DOWN"
    else:
        return False
'''

@register.simple_tag
def up_vote_exists(model, user=AnonymousUser(), action=UP):
    if user.is_anonymous():
        return False
    return model.votes.exists(user.pk, action=action)


@register.simple_tag
def down_vote_exists(model, user=AnonymousUser(), action=DOWN):
    if user.is_anonymous():
        return False
    return model.votes.exists(user.pk, action=action)