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

    def search(self, origin: str = None, destination: str = None, date: str = None, sort_by: str = None) -> List[Flight]:
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
                pass # Ignore invalid date format for now
        print(f"DEBUG: Search Query: {query}")
        
        sort_criteria = []
        if sort_by == 'price_asc':
            sort_criteria.append(('current_price', 1))
        elif sort_by == 'price_desc':
            sort_criteria.append(('current_price', -1))
        elif sort_by == 'duration_asc':
            pass 
        elif sort_by == 'duration_desc':
            pass
        else:
            sort_criteria.append(('current_price', 1))

        if sort_criteria:
            cursor = self.collection.find(query, {'_id': 0}).sort(sort_criteria)
        else:
            cursor = self.collection.find(query, {'_id': 0})
        results = [Flight(**doc) for doc in cursor]
        
        if sort_by == 'duration_asc':
            results.sort(key=lambda x: (x.arrival_time - x.departure_time).total_seconds())
        elif sort_by == 'duration_desc':
            results.sort(key=lambda x: (x.arrival_time - x.departure_time).total_seconds(), reverse=True)
            
        print(f"DEBUG: Found {len(results)} flights")
        return results

    def update_flight(self, flight: Flight):
        self.collection.update_one(
            {'flight_id': flight.flight_id},
            {'$set': flight.to_dict()}
        )

    def decrement_seats(self, flight_id: str, count: int):
        self.collection.update_one(
            {'flight_id': flight_id},
            {'$inc': {'available_seats': -count}}
        )

    def save_fare_history(self, history):
        from core.db import MongoDB
        db = MongoDB.get_db()
        db['fare_history'].insert_one(history.to_dict())

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
