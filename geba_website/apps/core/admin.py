from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ModelFormFailureHistory, User
# Register your models here.

admin.site.register(ModelFormFailureHistory)


class UserAdminCustom(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'id')

admin.site.register(User, UserAdminCustom)
