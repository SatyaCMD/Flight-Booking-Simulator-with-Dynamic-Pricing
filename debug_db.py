import os
import sys
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flight_simulator.settings')
django.setup()

from flights.repositories import FlightRepository

def debug_flights():
    repo = FlightRepository()
    total_count = repo.collection.count_documents({})
    print(f"Total flights in DB: {total_count}")
    
    if total_count == 0:
        print("No flights found in DB! You might need to run seed_flights.")
        return

    print("\nTesting Search (IST -> JFK for tomorrow)...")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    results = repo.search(origin="IST", destination="JFK", date=tomorrow)
    print(f"Found {len(results)} flights from IST to JFK on {tomorrow}")
    
    if results:
        print("Sample result:")
        print(f"  Flight: {results[0].flight_number}")
        print(f"  Price: {results[0].base_price}")
        print(f"  Dep: {results[0].departure_time}")
    else:
        print("No flights found for IST -> JFK!")
    print("\nTesting Search (JFK -> LHR for tomorrow)...")
    results = repo.search(origin="JFK", destination="LHR", date=tomorrow)
    print(f"Found {len(results)} flights from JFK to LHR on {tomorrow}")

if __name__ == "__main__":
    debug_flights()

