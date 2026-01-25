from django.db import models
from agencies.models import AgencyBranch
from utils.base_model import BaseModel

class BusCategory(models.TextChoices):
    CLASSIC = 'classic', 'Classic'
    VIP = 'vip', 'VIP'
    VVIP = 'vvip', 'VVIP'

class BusFeature(models.TextChoices):
    AC = 'ac', 'Air Conditioning'
    TV = 'tv', 'Television'
    WIFI = 'wifi', 'WiFi'
    TOILET = 'toilet', 'Toilet'
    USB_PORTS = 'usb_ports', 'USB Ports'
    RECLINING_SEATS = 'reclining_seats', 'Reclining Seats'
    READING_LIGHT = 'reading_light', 'Reading Light'
    BLANKET = 'blanket', 'Blanket'
    PILLOW = 'pillow', 'Pillow'
    WATER = 'water', 'Drinking Water'
    SNACKS = 'snacks', 'Snacks'
    CHARGING_PORTS = 'charging_ports', 'Charging Ports'
    ENTERTAINMENT = 'entertainment', 'Entertainment System'
    BERTHS = 'berths', 'Sleeping Berths'

class Bus(BaseModel):
    matriculation_code = models.CharField(max_length=50, unique=True)
    agency_branches = models.ManyToManyField(
        AgencyBranch,
        related_name='buses',
        help_text='Agencies this bus can work for'
    )
    category = models.CharField(
        max_length=20,
        choices=BusCategory.choices,
        default=BusCategory.CLASSIC
    )
    features = models.JSONField(
        default=list,
        help_text='List of features this bus has'
    )
    total_seats = models.PositiveSmallIntegerField()
    rows = models.PositiveSmallIntegerField(help_text='Number of seat rows')
    columns = models.PositiveSmallIntegerField(help_text='Number of seat columns')
    back_seat_count = models.PositiveSmallIntegerField(
        default=0,
        help_text='Number of seats in the back row (may be different from columns)'
    )
    has_toilet = models.BooleanField(default=False)
    has_ac = models.BooleanField(default=False)
    has_tv = models.BooleanField(default=False)
    has_wifi = models.BooleanField(default=False)
    registration_number = models.CharField(max_length=50, unique=True)
    manufacture_year = models.PositiveSmallIntegerField()
    last_maintenance_date = models.DateField(null=True, blank=True)
    next_maintenance_date = models.DateField(null=True, blank=True)
    insurance_expiry = models.DateField(null=True, blank=True)
    is_available = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Buses'
        ordering = ['matriculation_code']

    def __str__(self):
        return f"{self.get_category_display()} - {self.matriculation_code}"

    def save(self, *args, **kwargs):
        # Ensure features list is unique
        if isinstance(self.features, list):
            self.features = list(set(self.features))
        super().save(*args, **kwargs)