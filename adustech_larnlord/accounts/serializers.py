from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from listings.models import HouseListing 



class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'full_name', 'phone_number',
            'address', 'profile_picture', 'role', 'status', 'date_joined'
        ]
        read_only_fields = ['id', 'role', 'status', 'date_joined']


class LandlordRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)
    full_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    profile_picture = serializers.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = [
            'email', 'username', 'password', 'confirm_password',
            'full_name', 'phone_number', 'address', 'profile_picture'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        profile_picture = validated_data.pop('profile_picture', None)
# Explicitly extract only the fields you know are safe
        fields = {
        'email': validated_data['email'],
        'username': validated_data['username'],
        'password': validated_data['password'],
        'full_name': validated_data['full_name'],
        'phone_number': validated_data['phone_number'],
        'address': validated_data['address'],
    }
        user = CustomUser.objects.create_landlord(**fields)    

        if profile_picture:
            user.profile_picture = profile_picture
            user.save()

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'), email=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid credentials. Please try again.")

        if not user.is_active:
            raise serializers.ValidationError("Account is not active. Please wait for approval.")

        refresh = RefreshToken.for_user(user)

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
            }
        }


class LandlordApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['status']

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        if instance.status == 'Approved':
            instance.is_active = True
        instance.save()
        return instance

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'full_name', 'phone_number',
            'address', 'profile_picture'
        ]
        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': False},
            'full_name': {'required': False},
            'phone_number': {'required': False},
            'address': {'required': False},
            'profile_picture': {'required': False},
        }
#----------------------------Dashbored stuff------------------

#-----------Admin_Dashbored-------
class PendingLandlordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'email',
            'username',
            'full_name',
            'phone_number',
            'address',
            'profile_picture',
            'date_joined',
            'status',
        ]

class LandlordActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['is_approved', 'is_rejected', 'is_active', 'is_banned', 'status']

    def update(self, instance, validated_data):
        for field in self.Meta.fields:
            if field in validated_data:
               setattr(instance, field, validated_data[field])
        instance.save()
        return instance

class PropertyListingSerializer(serializers.ModelSerializer):
    landlord_name = serializers.SerializerMethodField()
    landlord_email = serializers.SerializerMethodField()

    class Meta:
        model = HouseListing
        fields = [
            'id',
            'email',
            'username',
            'full_name',
            'phone_number',
            'address',
            'profile_picture',
            'date_joined',
            'status',
        ]
        
        read_only_fields = fields
    def get_landlord_name(self, obj):
        return getattr(obj.landlord, 'full_name', obj.landlord.username)

    def get_landlord_email(self, obj):
        return obj.landlord.email
