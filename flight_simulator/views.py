from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def book_flight(request, flight_id):
    return render(request, 'booking.html', {'flight_id': flight_id})
