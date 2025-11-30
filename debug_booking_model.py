import os
import sys
import django
from dataclasses import fields

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flight_simulator.settings')
django.setup()

from flights.models import Booking

print("Booking fields:")
for f in fields(Booking):
    print(f"- {f.name}")

try:
    b = Booking(
        booking_reference="REF",
        transaction_id="TXN",
        user_email="test@test.com",
        flight_number="FL123",
        booking_date="2023-01-01",
        passenger_details=[],
        status="CONFIRMED"
    )
    print("\nBooking instantiation successful!")
except Exception as e:
    print(f"\nBooking instantiation failed: {e}")
