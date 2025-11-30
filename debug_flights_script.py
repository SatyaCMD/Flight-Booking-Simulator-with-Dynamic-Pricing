import os
import django
from datetime import datetime, timedelta
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flight_simulator.settings')
django.setup()

from flights.repositories import FlightRepository
from flights.models import Flight

def debug_flights():
    repo = FlightRepository()
    flights = repo.find_all()
    print(f"Total Flights in DB: {len(flights)}")
    
    print(f"Total Flights in DB: {len(flights)}")
    print("Seeding flights...")
    seed_flights(repo)

def seed_flights(repo):
    origins = ['JFK', 'LHR', 'LAX', 'SFO', 'DXB', 'SIN', 'HND', 'CDG']
    destinations = ['JFK', 'LHR', 'LAX', 'SFO', 'DXB', 'SIN', 'HND', 'CDG']
    airlines = ['AA', 'BA', 'DL', 'EK', 'SQ', 'JL', 'AF']
    
    new_flights = []
    start_date = datetime.now()
    for i in range(30):
        current_date = start_date + timedelta(days=i)
        
        for hour in [9, 14, 19]:
            departure = current_date.replace(hour=hour, minute=0, second=0, microsecond=0)
            arrival = departure + timedelta(hours=7)
            flight = Flight(
                flight_id=f"FL_JFK_LHR_{i}_{hour}",
                flight_number=f"BA{random.randint(100, 999)}",
                airline_code="BA",
                origin="JFK",
                destination="LHR",
                departure_time=departure,
                arrival_time=arrival,
                base_price=random.randint(400, 900),
                total_seats=300,
                available_seats=random.randint(100, 300)
            )
            new_flights.append(flight)

        for _ in range(5): 
            origin = random.choice(origins)
            dest = random.choice([d for d in destinations if d != origin])
            hour = random.randint(6, 22)
            minute = random.choice([0, 15, 30, 45])
            departure = current_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
            duration_hours = random.randint(2, 14)
            arrival = departure + timedelta(hours=duration_hours)
            
            flight = Flight(
                flight_id=f"FL{random.randint(10000, 99999)}",
                flight_number=f"{random.choice(airlines)}{random.randint(100, 999)}",
                airline_code=random.choice(airlines),
                origin=origin,
                destination=dest,
                departure_time=departure,
                arrival_time=arrival,
                base_price=random.randint(200, 1500),
                total_seats=200,
                available_seats=random.randint(50, 200)
            )
            new_flights.append(flight)
            
    repo.insert_many(new_flights)
    print(f"Seeded {len(new_flights)} flights.")

if __name__ == "__main__":
    debug_flights()

