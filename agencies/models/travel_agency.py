from django.db import models
from django.contrib.auth import get_user_model
from utils.base_model import BaseModel
from utils.image_upload_handler import handle_uploaded_file

User = get_user_model()


class TravelAgency(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    agency_logo = models.ImageField(
        upload_to=handle_uploaded_file,
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Travel Agencies"
