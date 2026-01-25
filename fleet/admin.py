from django.contrib import admin
from unfold.admin import ModelAdmin
from .models.bus import Bus

@admin.register(Bus)
class BusAdmin(ModelAdmin):
    list_display = (
        'matriculation_code', 'registration_number', 'get_category_display',
        'total_seats', 'is_available', 'created_at'
    )
    list_filter = ('category', 'is_available', 'has_ac', 'has_tv', 'has_wifi')
    search_fields = (
        'matriculation_code', 'registration_number', 
        'features', 'manufacture_year'
    )
    list_select_related = ()
    list_editable = ('is_available',)
    list_per_page = 20
    date_hierarchy = 'created_at'
    filter_horizontal = ('agency_branches',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'matriculation_code', 'registration_number', 'category',
                'manufacture_year'
            )
        }),
        ('Seating Configuration', {
            'fields': (
                'total_seats', 'rows', 'columns', 'back_seat_count'
            )
        }),
        ('Features', {
            'fields': (
                'features', 'has_ac', 'has_tv', 'has_wifi', 'has_toilet'
            )
        }),
        ('Maintenance', {
            'fields': (
                'last_maintenance_date', 'next_maintenance_date',
                'insurance_expiry', 'is_available'
            ),
            'classes': ('collapse',)
        }),
        ('Agencies', {
            'fields': ('agency_branches',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('agency_branches')