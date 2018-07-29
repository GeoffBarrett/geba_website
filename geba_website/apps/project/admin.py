from django.contrib import admin
# from django.urls import reverse
# from django.utils.html import format_html
from .models import ProjectPost, Project
# Register your models here.


class ProjectPostAdmin(admin.ModelAdmin):

    list_display = ('title', 'publish_date', 'id')
    # readonly_fields = ('show_url',)
    #
    # def show_url(self, instance):
    #     url = reverse("blog:detail", kwargs={"slug": instance.slug})
    #     response = format_html("""<a href="{0}">{1}</a>""", url, url)
    #     return response
    #
    # show_url.short_description = "Post URL"
    # show_url.allow_tags = True  # display HTML tags, never set to True for geba_auth submitted data


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_date', 'id')
    filter_horizontal = ('authors', 'pages')  # If you don't specify this, you will get a multiple select widget.
    # readonly_fields = ('show_url',)
    #
    # def show_url(self, instance):
    #     url = reverse("blog:detail", kwargs={"slug": instance.slug})
    #     response = format_html("""<a href="{0}">{1}</a>""", url, url)
    #     return response
    #
    # show_url.short_description = "Post URL"
    # show_url.allow_tags = True  # display HTML tags, never set to True for geba_auth submitted data

admin.site.register(ProjectPost, ProjectPostAdmin)
admin.site.register(Project, ProjectAdmin)
