from django.contrib import admin
from .models import Keyword
# Register your models here.


class KeywordAdmin(admin.ModelAdmin):

    list_display = ('keyword', 'id')


admin.site.register(Keyword, KeywordAdmin)
