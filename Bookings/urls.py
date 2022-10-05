from rest_framework.routers import DefaultRouter
from django.urls import path, include
from Bookings import views as bookings_views



router = DefaultRouter()
router.register(r'bookings', bookings_views.BookingViewSet, basename='bookings')

urlpatterns = [
    path('', include(router.urls)),
]