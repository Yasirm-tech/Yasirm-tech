from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LandlordViewSet, LandlordRegisterView, LoginView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import ProfileUpdateView
from .views import (
    PendingLandlordListView,
    LandlordActionView,
    AllPropertyListingsView,
    DeleteListingView,
)


router = DefaultRouter()
router.register(r'landlords', LandlordViewSet, basename='landlord')

urlpatterns = [
    path('register/landlord/', LandlordRegisterView.as_view(), name='landlord-register'),
    path('login/', LoginView.as_view(), name='login'),
    path('', include(router.urls)),  # Routes for landlord list, approve, etc.
    path('profile/update/', ProfileUpdateView.as_view(), name='profile-update'), 
    # 1️⃣ View all pending landlords
    path('admin/landlords/pending/', PendingLandlordListView.as_view(), name='pending-landlords'),

    # 2️⃣ Take action on a specific landlord (approve, reject, ban, etc.)
    path('admin/landlords/<int:pk>/action/', LandlordActionView.as_view(), name='landlord-action'),

    # 3️⃣ View all property listings (with landlord info)
    path('admin/listings/', AllPropertyListingsView.as_view(), name='all-property-listings'),

    # 4️⃣ Delete a specific listing
    path('admin/listings/<int:pk>/delete/', DeleteListingView.as_view(), name='delete-listing'), 
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
