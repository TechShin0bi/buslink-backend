from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import *
from unfold.admin import ModelAdmin

User = get_user_model()


@admin.register(TravelAgency)
class TravelAgencyAdmin(ModelAdmin):
    pass
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')

    

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    filter_horizontal = ('permissions',)
    search_fields = ('name', 'code')

@admin.register(AgencyEmployee)
class AgencyEmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'agency', 'role', 'is_active', 'date_joined')
    list_filter = ('is_active', 'role', 'agency')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'agency__name')
    list_select_related = ('user', 'agency', 'role')
    raw_id_fields = ('user',)

@admin.register(AgencyLocation)
class AgencyLocationAdmin(ModelAdmin):
    list_display = ('name', 'branch', 'is_active', 'created_at')
    search_fields = ('name', 'branch__name')
    list_select_related = ('branch',)

@admin.register(AgencyBranch)
class AgencyBranchAdmin(ModelAdmin):
    list_display = ('name', 'agency', 'created_at')
    list_filter = ('agency',)
    search_fields = ('name', 'agency__name')
    list_select_related = ('agency',)
    raw_id_fields = ('agency',)