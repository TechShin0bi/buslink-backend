from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'countries', views.CountryViewSet)
router.register(r'agencies', views.TravelAgencyViewSet)
router.register(r'agency-locations', views.AgencyLocationViewSet)

app_name = 'agencies'

urlpatterns = [
    path('', include(router.urls)),
]