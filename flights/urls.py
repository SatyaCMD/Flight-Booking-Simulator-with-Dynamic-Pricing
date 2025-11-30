from django.urls import path
from .views import FlightListView, FlightSearchView, AirportListView, FlightDetailView
from .auth_views import SignupView, LoginView, VerifyOTPView
from .booking_views import BookingCreateView, BookingListView, BookingCheckinView, BookingCancelView

urlpatterns = [
    path('', FlightListView.as_view(), name='flight-list'),
    path('search/', FlightSearchView.as_view(), name='flight-search'),
    path('airports/', AirportListView.as_view(), name='airport-list'),
    path('auth/signup/', SignupView.as_view(), name='signup'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('bookings/create/', BookingCreateView.as_view(), name='booking-create'),
    path('bookings/check-in/', BookingCheckinView.as_view(), name='booking-checkin'),
    path('bookings/cancel/<str:booking_id>/', BookingCancelView.as_view(), name='booking-cancel'),
    path('bookings/', BookingListView.as_view(), name='booking-list'),
    path('<str:flight_id>/', FlightDetailView.as_view(), name='flight-detail'),
]
