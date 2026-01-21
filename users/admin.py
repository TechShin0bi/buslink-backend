from django.contrib import admin

from django.contrib.auth.models import Group , Permission
from unfold.admin import ModelAdmin
from .models import User

@admin.register(User)
class UserAdmin(ModelAdmin):
    pass

@admin.register(Permission)
class PermissionAdmin(ModelAdmin):
    pass
