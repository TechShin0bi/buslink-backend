from django.db import models
from django.contrib.auth import get_user_model
from utils.base_model import BaseModel

User = get_user_model()

class AgencyEmployee(BaseModel):
    """
    Represents an employee's association with an agency and their role.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='agency_employments'
    )
    branch = models.ForeignKey(
        'AgencyBranch',
        on_delete=models.CASCADE,
        related_name='agency_employees'
    )
    role = models.ForeignKey(
        'Role',  
        on_delete=models.PROTECT,
        related_name='agency_employees'
    )
    is_active = models.BooleanField(default=True)
    date_joined = models.DateField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'branch')
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.role.name} at {self.branch.name}"