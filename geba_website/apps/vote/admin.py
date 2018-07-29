from django.contrib import admin
from .models import Vote
# Register your models here.


class VoteAdmin(admin.ModelAdmin):

    list_display = ('create_at', 'content_type', 'user_id', 'object_id', 'content_object')


admin.site.register(Vote, VoteAdmin)
