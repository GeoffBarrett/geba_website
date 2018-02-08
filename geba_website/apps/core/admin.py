from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ModelFormFailureHistory, User
# Register your models here.

admin.site.register(ModelFormFailureHistory)

admin.site.register(User, UserAdmin)