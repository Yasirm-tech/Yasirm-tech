#-----------landlordshabored_stuff----------
# core/serializers.py

from rest_framework import serializers
from listings.models import HouseListing, HouseImage
from django.contrib.auth import get_user_model
from accounts.models import CustomUser 

class LandlordDashboardCreateHouseListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseListing
        fields = ['house_type', 'location', 'price', 'contact', 'is_available']

    def create(self, validated_data):
        validated_data['landlord'] = self.context['request'].user
        return super().create(validated_data)

class LandlordDashboardHouseListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseListing
        fields = ['id', 'house_type', 'location', 'price', 'contact', 'is_available']
        read_only_fields = fields       

class LandlordDashboardUpdateHouseListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseListing
        fields = ['house_type', 'location', 'price', 'contact', 'is_available']

class LandlordDashboardProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser  # Assuming this is your user model
        fields = ['id', 'full_name', 'email', 'phone_number', 'role']
        read_only_fields = fields

class LandlordDashboardUploadHouseImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseImage
        fields = ['house_listing', 'image', 'caption']



