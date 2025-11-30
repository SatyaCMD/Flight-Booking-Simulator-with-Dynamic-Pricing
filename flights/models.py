from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Optional

@dataclass
class Airport:
    code: str  # IATA code, e.g., JFK
    name: str
    city: str
    country: str

    def to_dict(self):
        return asdict(self)

@dataclass
class Airline:
    code: str  # IATA code, e.g., AA
    name: str

    def to_dict(self):
        return asdict(self)

@dataclass
class Flight:
    flight_id: str # Unique ID for the flight instance
    flight_number: str
    airline_code: str
    origin: str  # Airport code
    destination: str  # Airport code
    departure_time: datetime
    arrival_time: datetime
    base_price: float
    total_seats: int
    available_seats: int
    status: str = "SCHEDULED"  # SCHEDULED, DELAYED, CANCELLED
    current_price: Optional[float] = None

    def __post_init__(self):
        if self.current_price is None:
            self.current_price = self.base_price

    def to_dict(self):
        return asdict(self)

@dataclass
class Booking:
    booking_reference: str  # PNR
    transaction_id: str # Unique Transaction ID
    user_email: str
    flight_number: str
    booking_date: datetime
    passenger_details: List[dict] # Name, Age, Seat Number, etc.
    status: str = "CONFIRMED"
    
    def to_dict(self):
        return asdict(self)

