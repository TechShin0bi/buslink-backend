from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Country, TravelAgency, AgencyLocation
from unfold.admin import ModelAdmin

User = get_user_model()

@admin.register(Country)
class CountryAdmin(ModelAdmin):
    list_display = ('name', 'code', 'created_at')
    search_fields = ('name', 'code')
    ordering = ('name',)

@admin.register(TravelAgency)
class TravelAgencyAdmin(ModelAdmin):
    list_display = ('name', 'country', 'owner', 'is_active', 'created_at')
    list_filter = ('country', 'is_active')
    search_fields = ('name', 'description', 'owner__email')
    list_select_related = ('country', 'owner')
    raw_id_fields = ('owner',)

@admin.register(AgencyLocation)
class AgencyLocationAdmin(ModelAdmin):
    list_display = ('name', 'agency', 'latitude', 'longitude', 'is_active')
    list_filter = ('is_active', 'agency__country')
    search_fields = ('name', 'agency__name')
    list_select_related = ('agency',)
    
    
    
# # agencies/admin.py
# from django.contrib import admin
# from django.contrib.auth.models import Permission
# from .models import Role, AgencyEmployee, TravelAgency, AgencyLocation, Country

# @admin.register(Role)
# class RoleAdmin(admin.ModelAdmin):
#     list_display = ('name', 'code')
#     filter_horizontal = ('permissions',)
#     search_fields = ('name', 'code')

# @admin.register(AgencyEmployee)
# class AgencyEmployeeAdmin(admin.ModelAdmin):
#     list_display = ('user', 'agency', 'role', 'is_active', 'date_joined')
#     list_filter = ('is_active', 'role', 'agency')
#     search_fields = ('user__email', 'user__first_name', 'user__last_name', 'agency__name')
#     list_select_related = ('user', 'agency', 'role')
#     raw_id_fields = ('user',)

# # Update the existing admin classes to show employees
# class AgencyEmployeeInline(admin.TabularInline):
#     model = AgencyEmployee
#     extra = 1
#     raw_id_fields = ('user',)

# @admin.register(TravelAgency)
# class TravelAgencyAdmin(admin.ModelAdmin):
#     # ... existing fields ...
#     inlines = [AgencyEmployeeInline]
#     # ... rest of the admin ...