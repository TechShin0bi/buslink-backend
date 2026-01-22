from django.db import models
from django.contrib.auth import get_user_model
from utils.base_model import BaseModel

User = get_user_model()

class Country(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=2, unique=True, help_text="2-letter country code (e.g., US, CA, GB)")
   

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Countries"


class TravelAgency(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='agencies')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_agencies')
    is_active = models.BooleanField(default=True)
   

    def __str__(self):
        return f"{self.name} ({self.country.code})"

    class Meta:
        verbose_name_plural = "Travel Agencies"


class AgencyLocation(BaseModel):
    agency = models.ForeignKey(TravelAgency, on_delete=models.CASCADE, related_name='locations')
    name = models.CharField(max_length=200, help_text="Name to identify this location (e.g., 'Main Office', 'Downtown Branch')")
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    is_active = models.BooleanField(default=True)
   

    class Meta:
        unique_together = ('agency', 'name')
        ordering = ['agency', 'name']

    def __str__(self):
        return f"{self.agency.name} - {self.name}"

    def get_coordinates(self):
        return (float(self.latitude), float(self.longitude))