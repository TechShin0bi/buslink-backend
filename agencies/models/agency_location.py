from django.db import models
from utils.base_model import BaseModel

class AgencyLocation(BaseModel):
    branch = models.ForeignKey(
        'AgencyBranch',
        on_delete=models.CASCADE, 
        related_name="branch_location"
    )
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at'] 

    def __str__(self):
        return f"{self.branch.name} Location ({self.latitude}, {self.longitude})"