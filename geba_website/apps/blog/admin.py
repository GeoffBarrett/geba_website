from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.html import format_html
from .models import Post
# Register your models here.


class PostAdmin(admin.ModelAdmin):

    list_display = ('title', 'publish_date', 'id')
    # readonly_fields = ('show_url',)
    #
    # def show_url(self, instance):
    #     url = reverse("blog:detail", kwargs={"slug": instance.slug})
    #     response = format_html("""<a href="{0}">{1}</a>""", url, url)
    #     return response
    #
    # show_url.short_description = "Post URL"
    # show_url.allow_tags = True  # display HTML tags, never set to True for user submitted data

admin.site.register(Post, PostAdmin)
