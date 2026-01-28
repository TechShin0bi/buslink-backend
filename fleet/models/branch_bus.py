from django.db import models
from fleet.models import Bus
from agencies.models import AgencyBranch
from utils.base_model import BaseModel

class BranchBus(BaseModel):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    agency_branch = models.ForeignKey(AgencyBranch, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)