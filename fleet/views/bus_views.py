from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from fleet.models import Bus
from fleet.serializers import BusSerializer, BusListSerializer
from utils.pagination import StandardResultsSetPagination

class BusViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing buses.
    """
    queryset = Bus.objects.all()
    serializer_class = BusSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    pagination_class = StandardResultsSetPagination
    search_fields = [
        'matriculation_code', 'registration_number', 'features',
        'manufacture_year'
    ]
    filterset_fields = {
        'category': ['exact'],
        'is_available': ['exact'],
        'has_ac': ['exact'],
        'has_tv': ['exact'],
        'has_wifi': ['exact'],
        'has_toilet': ['exact'],
        'agency_branches': ['exact'],
        'created_at': ['date', 'lte', 'gte'],
    }
    ordering_fields = [
        'matriculation_code', 'registration_number', 
        'manufacture_year', 'created_at'
    ]

    def get_serializer_class(self):
        if self.action == 'list':
            return BusListSerializer
        return self.serializer_class

    def get_queryset(self):
        queryset = super().get_queryset()
        # Add any custom filtering here
        return queryset

    @action(detail=True, methods=['post'])
    def toggle_availability(self, request, pk=None):
        """
        Toggle bus availability status.
        """
        bus = self.get_object()
        bus.is_available = not bus.is_available
        bus.save()
        return Response({
            'status': 'success',
            'is_available': bus.is_available
        })

    @action(detail=False, methods=['get'])
    def available(self, request):
        """
        Get all available buses.
        """
        buses = self.get_queryset().filter(is_available=True)
        page = self.paginate_queryset(buses)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(buses, many=True)
        return Response(serializer.data)