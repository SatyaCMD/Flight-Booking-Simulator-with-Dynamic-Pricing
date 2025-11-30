from datetime import datetime
from typing import List, Optional
from core.db import get_flights_collection
from .models import Flight, Booking

class FlightRepository:
    def __init__(self):
        self.collection = get_flights_collection()

    def insert_many(self, flights: List[Flight]):
        data = [f.to_dict() for f in flights]
        self.collection.insert_many(data)

    def find_all(self) -> List[Flight]:
        cursor = self.collection.find({}, {'_id': 0})
        return [Flight(**doc) for doc in cursor]

    def search(self, origin: str = None, destination: str = None, date: str = None) -> List[Flight]:
        query = {}
        if origin:
            query['origin'] = origin.upper()
        if destination:
            query['destination'] = destination.upper()
        
        if date:
            try:
                start_date = datetime.strptime(date, "%Y-%m-%d")
                end_date = start_date.replace(hour=23, minute=59, second=59)
                query['departure_time'] = {
                    '$gte': start_date,
                    '$lte': end_date
                }
            except ValueError:
                pass 

        print(f"DEBUG: Search Query: {query}")
        cursor = self.collection.find(query, {'_id': 0})
        results = [Flight(**doc) for doc in cursor]
        print(f"DEBUG: Found {len(results)} flights")
        return results

    def get_flight_by_id(self, flight_id: str) -> Optional[Flight]:
        doc = self.collection.find_one({'flight_id': flight_id}, {'_id': 0})
        if doc:
            return Flight(**doc)
        return None

    def delete_all(self):
        self.collection.delete_many({})

    def get_all_airports(self) -> List[str]:
        origins = self.collection.distinct('origin')
        destinations = self.collection.distinct('destination')
        return sorted(list(set(origins + destinations)))

class BookingRepository:
    def __init__(self):
        from core.db import get_bookings_collection
        self.collection = get_bookings_collection()

    def create(self, booking: Booking):
        self.collection.insert_one(booking.to_dict())
        return booking

    def get_by_user(self, email: str) -> List[Booking]:
        cursor = self.collection.find({'user_email': email}, {'_id': 0})
        return [Booking(**doc) for doc in cursor]

