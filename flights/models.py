from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Optional

@dataclass
class Airport:
    code: str  
    name: str
    city: str
    country: str

    def to_dict(self):
        return asdict(self)

@dataclass
class Airline:
    code: str  
    name: str

    def to_dict(self):
        return asdict(self)

@dataclass
class Flight:
    flight_id: str 
    flight_number: str
    airline_code: str
    origin: str  
    destination: str  
    departure_time: datetime
    arrival_time: datetime
    base_price: float
    total_seats: int
    available_seats: int
    seat_map: List[str]
    status: str = "SCHEDULED" 
    
    current_price: Optional[float] = None
    demand_level: float = 1.0 

    def __post_init__(self):
        if self.current_price is None:
            self.current_price = self.base_price

    def to_dict(self):
        return asdict(self)

@dataclass
class Booking:
    booking_reference: str 
    transaction_id: str 
    user_email: str
    flight_number: str
    booking_date: datetime
    passenger_details: List[dict] 
    flight_id: Optional[str] = None 
    travel_class: str = "Economy"
    status: str = "CONFIRMED"
    
    def to_dict(self):
        return asdict(self)



@dataclass
class FareHistory:
    flight_id: str
    price: float
    timestamp: datetime
    reason: str 

    def to_dict(self):
        return asdict(self)
