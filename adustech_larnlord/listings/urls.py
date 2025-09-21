from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListAllListingsView, ViewRetrieveListingDetail, LandlordHouseListing, HouseImageViewSet


router = DefaultRouter()
router.register(r'Listings', LandlordHouseListing, basename='Listings')
router.register(r'imageupload', HouseImageViewSet, basename='imageupload')

urlpatterns = [
    path('', include(router.urls)),
    path('listings/all/', ListAllListingsView.as_view(), name='list-all-listings'),
    path('listings/<int:pk>/', ViewRetrieveListingDetail.as_view(), name='retrieve-listing-detail')
]