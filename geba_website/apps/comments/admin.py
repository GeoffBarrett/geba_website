from django.contrib import admin

# Register your models here.

from .models import Comment


class CommentAdmin(admin.ModelAdmin):

    list_display = ('timestamp', 'author', 'content', 'object_id', 'parent', 'pk')
    # readonly_fields = ('show_url',)
    #
    # def show_url(self, instance):
    #     url = reverse("blog:detail", kwargs={"slug": instance.slug})
    #     response = format_html("""<a href="{0}">{1}</a>""", url, url)
    #     return response
    #
    # show_url.short_description = "Post URL"
    # show_url.allow_tags = True  # display HTML tags, never set to True for user submitted data

admin.site.register(Comment, CommentAdmin)
