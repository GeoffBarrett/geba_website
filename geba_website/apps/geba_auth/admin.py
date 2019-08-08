from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
# Register your models here.


class UserAdminCustom(UserAdmin):
    def __init__(self, *args, **kwargs):
        super(UserAdmin, self).__init__(*args, **kwargs)
        # UserAdmin.list_display = list(UserAdmin.list_display) + ['date_joined', 'some_function']
        # UserAdmin.fieldsets += list(UserAdmin.fieldsets) + ('email_confirmed')_

    list_display = ('username', 'id', 'email', 'first_name', 'last_name', 'is_staff', 'email_confirmed', 'date_joined',
                    'last_login')

    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('email_confirmed',)}), )


admin.site.register(User, UserAdminCustom)

