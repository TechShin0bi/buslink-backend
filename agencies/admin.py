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