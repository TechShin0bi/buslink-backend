from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import *
from unfold.admin import ModelAdmin
from django.utils.html import format_html

User = get_user_model()



@admin.register(TravelAgency)
class TravelAgencyAdmin(ModelAdmin):
    list_display = ('logo_thumbnail', 'name', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    readonly_fields = ('logo_thumbnail',)
    
    def logo_thumbnail(self, obj):
        if obj.agency_logo:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 50%; object-fit: cover;" />',
                obj.agency_logo.url
            )
        return "-"
    logo_thumbnail.short_description = 'Logo'
    logo_thumbnail.allow_tags = True


@admin.register(Role)
class RoleAdmin(ModelAdmin):
    list_display = ('name', 'code', 'created_at')
    list_filter = ('created_at',)  # Added comma here to make it a tuple
    search_fields = ('name', 'code', 'description')
    fieldsets = (
        ('Role Information', {
            'fields': ('name', 'code', 'description')
        }),
    )
    list_per_page = 20
    show_full_result_count = True
    date_hierarchy = 'created_at'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()
    

@admin.register(AgencyEmployee)
class AgencyEmployeeAdmin(ModelAdmin):  # Changed from admin.ModelAdmin to ModelAdmin
    list_display = ('user_full_name', 'branch', 'role', 'is_active', 'date_joined')
    list_filter = ('is_active', 'role', 'branch', 'date_joined')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'branch__name', 'role__name')
    list_select_related = ('user', 'branch', 'role')
    list_editable = ('is_active',)
    raw_id_fields = ('user',)
    date_hierarchy = 'date_joined'
    list_per_page = 20
    show_full_result_count = True
    
    fieldsets = (
        ('Employee Information', {
            'fields': ('user', 'branch', 'role')
        }),
        ('Status', {
            'fields': ('is_active', 'date_joined')
        }),
    )
    
    def user_full_name(self, obj):
        return obj.user.get_full_name() if obj.user else '-'
    user_full_name.short_description = 'Employee Name'
    user_full_name.admin_order_field = 'user__first_name'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'branch', 'role')


@admin.register(AgencyLocation)
class AgencyLocationAdmin(ModelAdmin):
    list_display = ('branch', 'is_active', 'created_at')
    search_fields = ('branch__name',)  # Make this a tuple with a comma
    list_select_related = ('branch',)
    list_filter = ('is_active', 'created_at')

@admin.register(AgencyBranch)
class AgencyBranchAdmin(ModelAdmin):
    list_display = ('name', 'agency', 'created_at')
    list_filter = ('agency',)
    search_fields = ('name', 'agency__name')
    list_select_related = ('agency',)
    raw_id_fields = ('agency',)