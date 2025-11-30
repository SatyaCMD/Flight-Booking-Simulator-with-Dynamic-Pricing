import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flight_simulator.settings')
django.setup()

from flights.repositories import BookingRepository

repo = BookingRepository()
result = repo.collection.delete_many({'transaction_id': {'$exists': False}})
print(f"Deleted {result.deleted_count} bookings missing transaction_id.")

result2 = repo.collection.delete_many({'passenger_details': {'$exists': False}})
print(f"Deleted {result2.deleted_count} bookings missing passenger_details.")

