from django.contrib import admin
from unfold.admin import ModelAdmin
from .models.bus import Bus

@admin.register(Bus)
class BusAdmin(ModelAdmin):
    list_display = (
        'matriculation_code', 'registration_number', 'get_category_display',
        'total_seats', 'created_at'
    )
    list_filter = ('category', 'has_ac', 'has_tv', 'has_wifi')
    search_fields = (
        'matriculation_code', 'registration_number', 
        'features', 
    )
    list_select_related = ()
    list_per_page = 20
    date_hierarchy = 'created_at'
    filter_horizontal = ('agency_branches',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'matriculation_code', 'registration_number', 'category',
                
            )
        }),
        ('Seating Configuration', {
            'fields': (
                'total_seats', 'columns', 'back_seat_count'
            )
        }),
        ('Features', {
            'fields': (
                'features', 'has_ac', 'has_tv', 'has_wifi', 'has_toilet'
            )
        }),
        ('Maintenance', {
            'fields': (
                'insurance_expiry',
            ),
            'classes': ('collapse',)
        }),
        ('Agencies', {
            'fields': ('agency_branches',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('agency_branches')