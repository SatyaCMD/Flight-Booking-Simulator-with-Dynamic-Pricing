import random
import time
from django.core.management.base import BaseCommand
from flights.repositories import FlightRepository
from flights.models import FareHistory
from flights.pricing import PricingEngine
from datetime import datetime

class Command(BaseCommand):
    help = 'Simulate market changes (demand, bookings, pricing)'

    def handle(self, *args, **options):
        self.stdout.write("Starting Market Simulation...")
        repo = FlightRepository()
        
        while True:
            try:
                flights = repo.find_all()
                self.stdout.write(f"Simulating for {len(flights)} flights...")
                
                for flight in flights:
                    if flight.available_seats > 0 and random.random() < 0.1: 
                        seats_booked = random.randint(1, 3)
                        flight.available_seats = max(0, flight.available_seats - seats_booked)
                        self.stdout.write(f"Flight {flight.flight_number}: {seats_booked} new bookings. Seats: {flight.available_seats}")

                    change = random.uniform(-0.1, 0.1)
                    flight.demand_level = max(0.5, min(2.0, flight.demand_level + change))
                    old_price = flight.current_price
                    new_price = PricingEngine.calculate_price(flight)
                    
                    if abs(new_price - old_price) > 1.0: 
                        flight.current_price = new_price
                        repo.update_flight(flight)
                        
                        history = FareHistory(
                            flight_id=flight.flight_id,
                            price=new_price,
                            timestamp=datetime.now(),
                            reason="Market Simulation"
                        )
                        repo.save_fare_history(history)
                        self.stdout.write(f"Flight {flight.flight_number}: Price updated ${old_price} -> ${new_price}")

                self.stdout.write("Simulation cycle complete. Sleeping...")
                time.sleep(10) 
                
            except KeyboardInterrupt:
                self.stdout.write("Stopping simulation.")
                break
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error in simulation: {e}"))
                time.sleep(5)
