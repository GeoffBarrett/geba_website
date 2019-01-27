from django.contrib import admin
# from django.urls import reverse
# from django.utils.html import format_html
from .models import ProjectPost, Project
from django.db import models
from tinymce.widgets import TinyMCE
# Register your models here.


class ProjectPostAdmin(admin.ModelAdmin):

    list_display = ('title', 'publish_date', 'id')

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_date', 'id')
    filter_horizontal = ('authors', 'pages')  # If you don't specify this, you will get a multiple select widget.

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }


admin.site.register(ProjectPost, ProjectPostAdmin)
admin.site.register(Project, ProjectAdmin)
