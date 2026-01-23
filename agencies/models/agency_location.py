from django.db import models
from utils.base_model import BaseModel

class AgencyLocation(BaseModel):
    branch = models.ForeignKey(
        'AgencyBranch',  
        on_delete=models.CASCADE, 
        related_name="branch_location"
    )
    name = models.CharField(
        max_length=200,
        help_text="Name to identify this location (e.g., 'Main Office', 'Downtown Branch')",
    )
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("branch", "name")
        ordering = ["branch", "name"]

    def __str__(self):
        return f"{self.branch.name} - {self.name}"

    def get_coordinates(self):
        return (float(self.latitude), float(self.longitude))