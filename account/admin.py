import datetime

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account.models import *


class AccountAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2', 'role',
                       'gender', 'birthday', 'image', 'bio',)}),)
    list_display = ('user_id', 'first_name', 'last_name', 'email', 'date_joined', 'role', 'is_admin')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('role',)
    exclude = ('password',)
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('email',)

    filter_horizontal = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)
