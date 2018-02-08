from __future__ import absolute_import
from django import template

register = template.Library()


# this simple tag will call a method on an object
# this will be used for annotating the comment votes
# but can be used for anything
@register.simple_tag
def children_annotate(comment, user_id):
    return comment.children(user_id)
