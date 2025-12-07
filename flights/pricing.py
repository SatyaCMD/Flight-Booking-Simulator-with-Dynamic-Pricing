from datetime import datetime, timedelta
from .models import Flight

class PricingEngine:
    @staticmethod
    def calculate_price(flight: Flight) -> float:
        """
        Calculate dynamic price based on:
        1. Base Price
        2. Time to departure (closer = more expensive)
        3. Available seats (scarcity = more expensive)
        4. Demand Level (simulated factor)
        """
        
        price = flight.base_price
        
        # 1. Time Factor
        now = datetime.now()
        if flight.departure_time > now:
            days_to_departure = (flight.departure_time - now).days
            
            if days_to_departure < 3:
                price *= 1.5  # Last minute surge
            elif days_to_departure < 7:
                price *= 1.3
            elif days_to_departure < 14:
                price *= 1.1
            elif days_to_departure > 60:
                price *= 0.8  # Early bird discount
        
        # 2. Scarcity Factor (Load Factor)
        if flight.total_seats > 0:
            load_factor = (flight.total_seats - flight.available_seats) / flight.total_seats
            
            if load_factor > 0.9:
                price *= 1.4 # Very few seats left
            elif load_factor > 0.7:
                price *= 1.2
            elif load_factor < 0.2:
                price *= 0.9 # Empty flight discount
                
        # 3. Demand Factor (Simulated)
        price *= flight.demand_level
        
        # Ensure price doesn't drop below a minimum threshold (e.g., 50% of base)
        min_price = flight.base_price * 0.5
        return max(round(price, 2), min_price)
