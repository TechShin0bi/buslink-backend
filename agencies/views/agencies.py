from agencies.models.agency_branch import AgencyBranch
from rest_framework import generics, status
from rest_framework.response import Response
from agencies.serializers import AgencyBranchSerializer
from agencies.serializers.agency_location import AgencyLocationSerializer
from rest_framework.permissions import IsAuthenticated
from utils.image_upload_handler import validate_and_upload_file

class GetTravelAgencyBranches(generics.ListAPIView):
    serializer_class = AgencyBranchSerializer
    queryset = AgencyBranch.objects.all()

    def get_queryset(self):
        agency_id = self.kwargs.get('agency_id')
        return self.queryset.filter(agency__id=agency_id)


class CreateAgencyBranchWithLocation(generics.CreateAPIView):
    """
    Create a new agency branch with its location and optional image.
    
    Expected payload (multipart/form-data):
    {
        "name": "Branch Name",
        "contact": "0712345678",
        "address": "123 Main St",
        "agency": 1,
        "image": <file>,  # Optional
        "location": {
            "latitude": "4.053544519648043",
            "longitude": "9.738178249055299",
            "is_active": true
        }
    }
    """
    serializer_class = AgencyBranchSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        # Extract location data from request
        location_data = request.data.pop('location', None)
        
        # Handle image upload if provided
        if 'image' in request.FILES:
            image_file = request.FILES['image']
            upload_result = validate_and_upload_file(image_file, 'agency_branches/')
            
            if not upload_result['success']:
                return Response(
                    {'error': upload_result['error']},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Don't add to request.data since ImageField will handle file upload
            # Just validate the file, it will be handled by the model's upload_to
        
        # Create the branch first
        branch_serializer = self.get_serializer(data=request.data)
        branch_serializer.is_valid(raise_exception=True)
        branch = branch_serializer.save()
        
        # Create location if provided
        if location_data:
            location_data['branch'] = branch.id
            location_serializer = AgencyLocationSerializer(data=location_data)
            location_serializer.is_valid(raise_exception=True)
            location_serializer.save()
        
        headers = self.get_success_headers(branch_serializer.data)
        return Response(branch_serializer.data, status=status.HTTP_201_CREATED, headers=headers)