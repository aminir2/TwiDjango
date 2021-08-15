from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

UserAdmin.fieldsets += (
    ("status on site", {'fields': ('avatar',
                                   )}),
)
UserAdmin.list_display += ('consumer_key', 'consumer_secret', 'access_token', 'access_token_secret','avatar')
admin.site.register(User, UserAdmin)
