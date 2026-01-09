from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .repositories import FlightRepository
from .models import Flight

class FlightListView(APIView):
    def get(self, request):
        repo = FlightRepository()
        flights = repo.find_all()
        return Response([f.to_dict() for f in flights])

class FlightSearchView(APIView):
    def get(self, request):
        origin = request.query_params.get('origin')
        destination = request.query_params.get('destination')
        date = request.query_params.get('date')
        sort_by = request.query_params.get('sort_by')

        if not origin or not destination:
            return Response(
                {"error": "Origin and destination are required parameters."},
                status=status.HTTP_400_BAD_REQUEST
            )

        repo = FlightRepository()
        flights = repo.search(origin, destination, date, sort_by)
        return Response([f.to_dict() for f in flights])

class AirportListView(APIView):
    def get(self, request):
        repo = FlightRepository()
        airports = repo.get_all_airports()
        return Response(airports)

class FlightDetailView(APIView):
    def get(self, request, flight_id):
        print(f"DEBUG: Fetching flight with ID: {flight_id}")
        repo = FlightRepository()
        flight = repo.get_flight_by_id(flight_id)
        if flight:
            print(f"DEBUG: Found flight: {flight.flight_number}")
            return Response(flight.to_dict())
        print("DEBUG: Flight not found")
        return Response({'error': 'Flight not found'}, status=status.HTTP_404_NOT_FOUND)

class SeatMapView(APIView):
    def get(self, request, flight_id):
        repo = FlightRepository()
        flight = repo.get_flight_by_id(flight_id)
        if not flight:
            return Response({'error': 'Flight not found'}, status=status.HTTP_404_NOT_FOUND)

        seat_map_list = []
        for row_index, row_str in enumerate(flight.seat_map):
            row_list = []
            col_index = 0
            for char in row_str:
                if char == 'X':
                    continue
                
                seat_class = "Economy"
                if row_index < 2:
                    seat_class = "First"
                elif row_index < 6:
                    seat_class = "Business"

                row_list.append({
                    "seat_number": f"{row_index + 1}{chr(65 + col_index)}",
                    "seat_class": seat_class,
                    "is_occupied": char == 'U'
                })
                col_index += 1
            seat_map_list.append(row_list)
        
        response_data = {
            "seat_map": seat_map_list,
            "layout": { "columns_per_side": 3 }
        }
        return Response(response_data)
