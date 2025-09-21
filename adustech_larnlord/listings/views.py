from rest_framework.viewsets import ModelViewSet
from .models import HouseListing, HouseImage
from .serializers import HouseListingSerializer, HouseImageSerializer
from accounts.permissions import IsLandlord
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response

class LandlordHouseListing(ModelViewSet):
    serializer_class = HouseListingSerializer
    permission_classes = [IsAuthenticated, IsLandlord]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['location', 'price', 'landlord', 'house_type', 'is_available']
    search_fields = ['location', 'house_type']

    def get_queryset(self):
        return  HouseListing.objects.filter(landlord=self.request.user)

    def perform_create(self, serializer):
        serializer.save(landlord=self.request.user)

    @action(detail=True, methods=['post'])
    def toggle_availability(self, request, pk=None):
        house = self.get_object()
        house.is_available = not house.is_available
        house.save()
        return Response({'status': 'availability updated', 'is_available': house.is_available}, status=status.HTTP_200_OK)

class HouseImageViewSet(ModelViewSet):
    serializer_class = HouseImageSerializer
    permission_classes = [IsAuthenticated, IsLandlord]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['caption', 'house_listing']
    search_fields = ['caption']

    def get_queryset(self):
        return HouseImage.objects.filter(house_listing__landlord=self.request.user)

    def perform_create(self, serializer):
        house_listing = serializer.validated_data['house_listing']
        if house_listing.landlord != self.request.user:
            raise PermissionDenied("You do not own this house listing.")
        serializer.save()
 
class ListAllListingsView(generics.ListAPIView):
    queryset = HouseListing.objects.all()
    serializer_class = HouseListingSerializer
    permission_classes = [] 
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['location', 'price', 'landlord', 'house_type', 'is_available']
    search_fields = ['location', 'house_type']

class ViewRetrieveListingDetail(generics.RetrieveAPIView):
    queryset = HouseListing.objects.all()
    serializer_class = HouseListingSerializer
    permission_classes = []
    pagination_class = None



