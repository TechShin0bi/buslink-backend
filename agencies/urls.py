from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# agencies/urls.py
router = DefaultRouter()
# ... existing registrations ...
router.register(r'agency-employees', AgencyEmployeeViewSet)
router.register(r'agency-roles', RoleViewSet)
router.register(r'countries', views.CountryViewSet)
router.register(r'agencies', views.TravelAgencyViewSet)
router.register(r'agency-locations', views.AgencyLocationViewSet)

app_name = 'agencies'

urlpatterns = [
    path('', include(router.urls)),
]