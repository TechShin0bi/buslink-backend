from django.db import models
from django.contrib.auth import get_user_model
from utils.base_model import BaseModel

User = get_user_model()

class AgencyBranch(BaseModel):
    name = models.CharField(max_length=200)
    agency = models.ForeignKey(
        'TravelAgency',
        on_delete=models.CASCADE,
        related_name="branches"
    )
    employees = models.ManyToManyField(
        User,
        through='AgencyEmployee',
        through_fields=('agency', 'user'),
        related_name='employing_agencies'
    )

    def __str__(self):
        return f"{self.name}"
