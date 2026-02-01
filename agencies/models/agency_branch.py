from django.db import models
from django.contrib.auth import get_user_model
from utils.base_model import BaseModel
from utils.image_upload_handler import handle_uploaded_file

User = get_user_model()

class AgencyBranch(BaseModel):
    name = models.CharField(max_length=200)
    contact = models.CharField(max_length=15)
    address = models.TextField()
    image = models.ImageField(
        upload_to=handle_uploaded_file,
        null=True,
        blank=True,
        help_text='Branch image/logo'
    )
    agency = models.ForeignKey(
        'TravelAgency',
        on_delete=models.CASCADE,
        related_name="branches"
    )

    def __str__(self):
        return f"{self.name}"
