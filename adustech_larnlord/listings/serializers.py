from rest_framework import serializers
from .models import HouseListing, HouseImage
from django.contrib.auth import authenticate


class HouseImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseImage
        fields = ['id', 'image', 'house_listing', 'caption']
        read_only_fields = ['id']   

class HouseListingSerializer(serializers.ModelSerializer):
    images = HouseImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = HouseListing
        fields = ['id','landlord', 'house_type', 'location', 'price', 'contact', 'is_available']
        read_only_fields = ['id','landlord','is_available']

    # Validation: price should not be negative
    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value    

    # Validation: contact must be a phone number or email
    def validate_contact(self, value):
        from django.core.validators import validate_email
        import re

        # Simple phone regex (e.g., 080..., +234..., etc.)
        phone_regex = r'^\+?\d{10,15}$'

        try:
            validate_email(value)  # valid email
            return value
        except Exception:
            # If not an email, check phone format
            if not re.match(phone_regex, value):
                raise serializers.ValidationError(
                    "Contact must be a valid email or phone number."
                )
        return value    

