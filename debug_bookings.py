import os
import sys
import django
from pprint import pprint

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flight_simulator.settings')
django.setup()

from flights.repositories import BookingRepository

repo = BookingRepository()
bookings = repo.collection.find({})
print(f"Found {repo.collection.count_documents({})} bookings.")

for b in bookings:
    print(f"\nBooking ID: {b.get('_id')}")
    missing = []
    if 'transaction_id' not in b: missing.append('transaction_id')
    if 'passenger_details' not in b: missing.append('passenger_details')
    
    if missing:
        print(f"  MISSING FIELDS: {missing}")
    else:
        print("  Valid.")
