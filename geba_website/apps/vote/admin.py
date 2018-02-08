from django.contrib import admin
from .models import Vote, VoteModel
# Register your models here.


class VoteAdmin(admin.ModelAdmin):

    list_display = ('create_at', 'content_type', 'user_id')

admin.site.register(Vote, VoteAdmin)