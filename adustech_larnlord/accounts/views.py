from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import  viewsets, status
from .serializers import (
CustomUserSerializer,
LandlordRegisterSerializer,
LandlordApprovalSerializer, 
ProfileSerializer,
PendingLandlordSerializer,
LandlordActionSerializer,
PropertyListingSerializer
)
from .serializers import LoginSerializer
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from .permissions import IsSuperAdmin, IsLandlord
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404
from listings.models import HouseListing


# accounts/views.py
class LandlordRegisterView(APIView):
    def post(self, request):
        serializer = LandlordRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Registration successful. Please wait for approval."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LandlordViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.filter(role='landlord')
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin] 

    @action(detail=True, methods=['post'], url_path='approve', permission_classes=[IsSuperAdmin])
    def approve_landlord(self, request, pk=None):
        landlord = self.get_object()

        if landlord.is_active and landlord.status == 'Approved':
            return Response({"message": "Landlord is already approved."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = LandlordApprovalSerializer(landlord, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Landlord approved successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileUpdateView(APIView):
    permission_classes =  [IsAuthenticated, IsLandlord] 

    def put(self, request):
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully."})
        return Response(serializer.errors, status=400)
               
#----------------------------Dashbored stuff------------------

#-----------Admin_Dashbored-------

class   PendingLandlordListView(ListAPIView):
    queryset = CustomUser.objects.filter(role="landlord", status="Pending")
    serializer_class = PendingLandlordSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

class LandlordActionView(APIView):
    permission_classes = [IsSuperAdmin]

    def patch(self, request, pk):
        landlord = get_object_or_404(CustomUser, pk=pk, role="landlord")
        serializer = LandlordActionSerializer(landlord, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Landlord action applied successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
    
class AllPropertyListingsView(ListAPIView):
    queryset = HouseListing.objects.all()
    serializer_class = PropertyListingSerializer
    permission_classes = [IsSuperAdmin]    

class DeleteListingView(APIView):
    permission_classes = [IsSuperAdmin]

    def delete(self, request, pk):
        listing = get_object_or_404(HouseListing, pk=pk)
        listing.delete()
        return Response({"message": "Listing deleted successfully."}, status=status.HTTP_204_NO_CONTENT)