from django.urls import path, include
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('book/<str:flight_id>/', views.book_flight, name='book_flight'),
    path('api/flights/', include('flights.urls')),  
    path('my-trips/', TemplateView.as_view(template_name='my_trips.html'), name='my_trips'),
    path('check-in/', TemplateView.as_view(template_name='checkin.html'), name='checkin'),
    path('profile/', TemplateView.as_view(template_name='profile.html'), name='profile'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),
    path('privacy/', TemplateView.as_view(template_name='privacy.html'), name='privacy'),
    path('terms/', TemplateView.as_view(template_name='terms.html'), name='terms'),
]
