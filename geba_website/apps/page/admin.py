from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.html import format_html
from .models import Page
# Register your models here.


class PageAdmin(admin.ModelAdmin):

    list_display = ('title',)
    readonly_fields = ('show_url',)

    def show_url(self, instance):
        url = reverse("page:detail", kwargs={"slug": instance.slug})
        response = format_html("""<a href="{0}">{1}</a>""", url, url)
        return response

    show_url.short_description = "Page URL"
    show_url.allow_tags = True  # display HTML tags, never set to True for user submitted data

#admin.site.register(Page, PageAdmin)
