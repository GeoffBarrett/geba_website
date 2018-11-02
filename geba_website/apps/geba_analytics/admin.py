from django.contrib import admin
from .models import ObjectViewed, UserSession
# Register your models here.

'''
class ObjectViewedAdmin(admin.ModelAdmin):

    list_display = ('content_type', 'user', 'timestamp')
'''

# admin.site.register(ObjectViewed, ObjectViewedAdmin)
admin.site.register(ObjectViewed)

admin.site.register(UserSession)
