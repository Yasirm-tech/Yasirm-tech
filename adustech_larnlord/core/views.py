#-------------landlorddasbored_stuff----
# core/views.py
from rest_framework import generics,  permissions
from listings.models import HouseImage, HouseListing
from listings.serializers import HouseListingSerializer
from .serializers import (
LandlordDashboardCreateHouseListingSerializer,
LandlordDashboardHouseListingSerializer,
LandlordDashboardUpdateHouseListingSerializer,
LandlordDashboardProfileSerializer,
LandlordDashboardUploadHouseImageSerializer

)
from accounts.permissions import IsLandlord
from rest_framework.exceptions import PermissionDenied


class LandlordDashboardCreateHouseListingView(generics.CreateAPIView):
    queryset = HouseListing.objects.all()
    serializer_class = LandlordDashboardCreateHouseListingSerializer
    permission_classes = [IsLandlord]

    def perform_create(self, serializer):
        serializer.save(landlord=self.request.user)

class LandlordDashboardHouseListingListView(generics.ListAPIView):
    queryset = HouseListing.objects.none()  # Default placeholder
    serializer_class = LandlordDashboardHouseListingSerializer
    permission_classes = [IsLandlord]

    def get_queryset(self):
        return HouseListing.objects.filter(landlord=self.request.user)

class LandlordDashboardUpdateHouseListingView(generics.UpdateAPIView):
    queryset = HouseListing.objects.all()
    serializer_class =  LandlordDashboardUpdateHouseListingSerializer
    permission_classes = [IsLandlord]

    def get_queryset(self):
        return HouseListing.objects.filter(landlord=self.request.user)
    
class LandlordDashboardProfileView(generics.RetrieveAPIView):
    serializer_class = LandlordDashboardProfileSerializer
    permission_classes = [IsLandlord]

    def get_object(self):
        return self.request.user    
    
class LandlordDashboardUploadHouseImageView(generics.CreateAPIView):
    queryset = HouseImage.objects.all()
    serializer_class = LandlordDashboardUploadHouseImageSerializer
    permission_classes = [IsLandlord]

    def perform_create(self, serializer):
        house_listing = serializer.validated_data['house_listing']
        if house_listing.landlord != self.request.user:
            raise PermissionDenied("You do not own this house listing.")
        serializer.save()    
