
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

def verify_filtering_logic():
    flight_repo = FlightRepository()
    booking_repo = BookingRepository()
    flight_num = "TF_FILTER_999"
    future_date = datetime(2026, 12, 25, 10, 0, 0)
    flight = Flight(
        flight_id="FLIGHT_ID_FUTURE",
        flight_number=flight_num,
        airline_code="TS",
        origin="SFO",
        destination="LHR",
        departure_time=future_date,
        arrival_time=future_date,
        base_price=500.0,
        total_seats=100,
        available_seats=100,
        seat_map=["A" * 6] * 20
    )
    flight_repo.insert_many([flight])
    
    user_email = "test_filter@example.com"
    booking_date = datetime(2025, 1, 1, 10, 0, 0) 
    booking = Booking(
        booking_reference="REF_FILTER_123",
        transaction_id="TXN_FILTER_123",
        user_email=user_email,
        flight_number=flight_num,
        booking_date=booking_date,
        passenger_details=[{"name": "Test User"}],
        flight_id="FLIGHT_ID_BROKEN", 
        travel_class="Economy",
        status="CONFIRMED"
    )
    
    booking_repo.collection.delete_one({'booking_reference': "REF_FILTER_123"})
    booking_repo.create(booking)
    
    print("\n--- Verifying BookingListView Output ---")
    bookings = booking_repo.get_by_user(user_email)
    
    for b in bookings:
        if b.booking_reference == "REF_FILTER_123":
            b_dict = b.to_dict()
            
            if b.flight_id:
                flight = flight_repo.get_flight_by_id(b.flight_id)
                is_fallback = False
                
                if not flight and b.flight_number:
                    flight = flight_repo.get_flight_by_number(b.flight_number)
                    is_fallback = True
                
                if flight:
                    details = {
                        'origin': flight.origin,
                        'destination': flight.destination,
                        'airline_code': flight.airline_code
                    }
                    if not is_fallback:
                        details['departure_time'] = flight.departure_time
                        details['arrival_time'] = flight.arrival_time
                    
                    b_dict['flight_details'] = details
            
            print(json.dumps(b_dict, cls=DateTimeEncoder, indent=2))
            
            if 'departure_time' not in b_dict.get('flight_details', {}):
                print("\nSUCCESS: 'departure_time' is MISSING in flight_details (Correct for fallback)")
                print("Frontend will use 'booking_date':", b_dict['booking_date'])
                
                booking_dt = b_dict['booking_date']
                if isinstance(booking_dt, str):
                    booking_dt = datetime.fromisoformat(booking_dt)
                
                now = datetime.now()
                if booking_dt < now:
                    print("Frontend Logic: Booking Date is in PAST -> COMPLETED (Correct)")
                else:
                    print("Frontend Logic: Booking Date is in FUTURE -> UPCOMING (Incorrect)")
            else:
                print("\nFAILURE: 'departure_time' IS present (Incorrect for fallback)")

if __name__ == "__main__":
    verify_filtering_logic()
