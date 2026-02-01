from django.urls import path, include
from agencies.views import *

urlpatterns = [
    path('agencies/<uuid:agency_id>/branches/', GetTravelAgencyBranches.as_view(), name='get_travel_agency_branches'),
    path('agencies/new/', CreateAgencyBranchWithLocation.as_view(), name='create_agency_branch_with_location'),
]