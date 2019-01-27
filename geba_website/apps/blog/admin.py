from django.contrib import admin
# from django.core.urlresolvers import reverse
# from django.utils.html import format_html
from .models import Post
from django.db import models
from tinymce.widgets import TinyMCE
# Register your models here.


class PostAdmin(admin.ModelAdmin):

    list_display = ('title', 'publish_date', 'id')

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }


admin.site.register(Post, PostAdmin)

