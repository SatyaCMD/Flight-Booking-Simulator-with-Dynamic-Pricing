from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
import random
from flights.models import Flight
from flights.repositories import FlightRepository
import uuid

class Command(BaseCommand):
    help = 'Seeds the database with simulated flight data'

    def handle(self, *args, **options):
        repo = FlightRepository()
        repo.delete_all() 

        airlines = ['AA', 'DL', 'UA', 'BA', 'LH', 'EK', 'SQ', 'QF', 'NH', 'AF', 'TK', 'QR', 'CX', 'VS']
        airports = ['JFK', 'LHR', 'LAX', 'DXB', 'SIN', 'HND', 'CDG', 'AMS', 'SYD', 'FRA', 'IST', 'ORD', 'ATL', 'PEK', 'CAN', 'SFO', 'MIA', 'YYZ', 'BOM', 'DEL']
        
        flights = []
        base_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        self.stdout.write("Generating flights... this may take a moment.")
        for origin in airports:
            for destination in airports:
                if origin == destination:
                    continue
                
                for day_offset in range(-2, 46):
                    current_date = base_date + timedelta(days=day_offset)
                    num_flights_today = random.randint(12, 15)
                    hours = sorted([random.randint(0, 23) for _ in range(num_flights_today)])
                    
                    for hour in hours:
                        minute = random.randint(0, 59)
                        departure = current_date.replace(hour=hour, minute=minute)
                        route_hash = hash(origin + destination)
                        base_duration_hours = (route_hash % 12) + 2 
                        duration_variance = random.randint(-30, 30) 
                        
                        duration_minutes = (base_duration_hours * 60) + duration_variance
                        arrival = departure + timedelta(minutes=duration_minutes)
                        airline = random.choice(airlines)
                        
                        base_cost = 100 + (base_duration_hours * 50) 
                        price_variance = random.randint(-50, 200)
                        price = base_cost + price_variance
                        
                        flight = Flight(
                            flight_id=str(uuid.uuid4()),
                            flight_number=f"{airline}{random.randint(1000, 9999)}",
                            airline_code=airline,
                            origin=origin,
                            destination=destination,
                            departure_time=departure,
                            arrival_time=arrival,
                            base_price=float(price),
                            total_seats=random.choice([180, 200, 250, 300]),
                            available_seats=random.randint(10, 180)
                        )
                        flights.append(flight)
                        if len(flights) >= 5000:
                            repo.insert_many(flights)
                            flights = []
                            self.stdout.write(f"Inserted batch... current date: {current_date.date()}")

        if flights:
            repo.insert_many(flights)
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded database. All routes covered.'))
