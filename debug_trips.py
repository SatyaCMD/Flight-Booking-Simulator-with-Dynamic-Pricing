
import os
import django
import sys
import json
from datetime import datetime

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flight_simulator.settings')
django.setup()

from flights.models import Flight, Booking
from flights.repositories import FlightRepository, BookingRepository

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

def debug_api():
    flight_repo = FlightRepository()
    booking_repo = BookingRepository()
    user_email = "test_fix@example.com" 
    all_bookings = list(booking_repo.collection.find({}))
    if all_bookings:
        user_email = all_bookings[0].get('user_email')
    
    print(f"Debugging bookings for: {user_email}")
    bookings = booking_repo.get_by_user(user_email)
    
    results = []
    for booking in bookings:
        b_dict = booking.to_dict()
        if booking.flight_id:
            flight = flight_repo.get_flight_by_id(booking.flight_id)
            
            if not flight and booking.flight_number:
                flight = flight_repo.get_flight_by_number(booking.flight_number)
            
            if flight:
                b_dict['flight_details'] = {
                    'origin': flight.origin,
                    'destination': flight.destination,
                    'departure_time': flight.departure_time,
                    'arrival_time': flight.arrival_time,
                    'airline_code': flight.airline_code
                }
        results.append(b_dict)
    print(json.dumps(results, cls=DateTimeEncoder, indent=2))

if __name__ == "__main__":
    debug_api()
