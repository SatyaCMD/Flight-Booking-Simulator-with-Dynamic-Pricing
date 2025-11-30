"""
This Part taken reference from python for Data Science
URL configuration for flight_simulator project.
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/flights/', include('flights.urls')),
    path('', lambda request: render(request, 'index.html'), name='home'),
    path('login/', lambda request: render(request, 'login.html'), name='login'),
    path('my-trips/', lambda request: render(request, 'my_trips.html'), name='my-trips'),
    path('check-in/', lambda request: render(request, 'checkin.html'), name='check-in'),
    path('book/<str:flight_id>/', lambda request, flight_id: render(request, 'booking.html'), name='book-flight'),
    path('profile/', lambda request: render(request, 'profile.html'), name='profile'),
]
