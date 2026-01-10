from flights.repositories import FlightRepository
from flights.models import Flight

def reset_seats():
    repo = FlightRepository()
    flights = repo.find_all()
    
    for flight in flights:
        print(f"Checking flight {flight.flight_number}...")
        updated = False
        new_map = []
        for row in flight.seat_map:
            if 'U' in row:
                print(f"  Found occupied seats in row: {row}")
                new_row = row.replace('U', 'A')
                new_map.append(new_row)
                updated = True
                print(f"  Reset to: {new_row}")
            else:
                new_map.append(row)
        
        if updated:
            flight.seat_map = new_map
            total_seats = sum(row.count('A') for row in new_map)
            
            repo.update_flight(flight)
            print(f"  Updated flight {flight.flight_number}")

if __name__ == "__main__":
    reset_seats()
