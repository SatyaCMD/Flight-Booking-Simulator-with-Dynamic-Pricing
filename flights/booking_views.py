from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .repositories import BookingRepository, FlightRepository
from .models import Booking
from datetime import datetime
import uuid
import random
import string

class BookingCreateView(APIView):
    def post(self, request):
        data = request.data
        user_email = data.get('user_email')
        flight_number = data.get('flight_number')
        flight_id = data.get('flight_id')
        passenger_details = data.get('passenger_details')
        travel_class = data.get('travel_class', 'Economy')
        
        if not user_email or not flight_number:
            return Response({'error': 'User email and flight number are required'}, status=status.HTTP_400_BAD_REQUEST)
            
        if not passenger_details or not isinstance(passenger_details, list) or len(passenger_details) == 0:
            return Response({'error': 'At least one passenger is required'}, status=status.HTTP_400_BAD_REQUEST)

        transaction_id = "TXN" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

        for passenger in passenger_details:
            preference = passenger.get('seat_preference', 'Any')
            row = random.randint(1, 30)
            if preference == 'Window':
                col = random.choice(['A', 'F'])
            elif preference == 'Aisle':
                col = random.choice(['C', 'D'])
            else: 
                col = random.choice(['B', 'E'])
            passenger['seat_number'] = f"{row}{col}"

        booking = Booking(
            booking_reference=str(uuid.uuid4())[:8].upper(),
            transaction_id=transaction_id,
            user_email=user_email,
            flight_number=flight_number,
            booking_date=datetime.now(),
            passenger_details=passenger_details,
            flight_id=flight_id,
            travel_class=travel_class,
            status="CONFIRMED"
        )

        repo = BookingRepository()
        repo.create(booking)
        flight_repo = FlightRepository()
        flight_repo.decrement_seats(flight_id, len(passenger_details))

        return Response({
            'message': 'Booking created successfully',
            'booking': booking.to_dict()
        }, status=status.HTTP_201_CREATED)

class BookingListView(APIView):
    def get(self, request):
        email = request.query_params.get('email')
        if not email:
            return Response({'error': 'Email parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        repo = BookingRepository()
        bookings = repo.get_by_user(email)
        flight_repo = FlightRepository()
        results = []
        for booking in bookings:
            b_dict = booking.to_dict()
            if booking.flight_id:
                flight = flight_repo.get_flight_by_id(booking.flight_id)
                if flight:
                    b_dict['flight_details'] = {
                        'origin': flight.origin,
                        'destination': flight.destination,
                        'departure_time': flight.departure_time,
                        'arrival_time': flight.arrival_time,
                        'airline_code': flight.airline_code
                    }
            results.append(b_dict)
        return Response(results)

class BookingCheckinView(APIView):
    def post(self, request):
        pnr = request.data.get('pnr')
        lastname = request.data.get('lastname')

        if not pnr or not lastname:
            return Response({'error': 'PNR and Last Name are required'}, status=status.HTTP_400_BAD_REQUEST)

        repo = BookingRepository()
        booking_doc = repo.collection.find_one({'booking_reference': pnr.upper()})
        
        if not booking_doc:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
        if '_id' in booking_doc:
            del booking_doc['_id']
            
        booking = Booking(**booking_doc)
        passenger_found = False
        for p in booking.passenger_details:
            if lastname.lower() in p.get('name', '').lower():
                passenger_found = True
                break
        
        if not passenger_found:
            return Response({'error': 'Passenger not found in this booking'}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'message': 'Booking found',
            'booking': booking.to_dict()
        })

class BookingCancelView(APIView):
    def post(self, request, booking_id):
        repo = BookingRepository()
        result = repo.collection.delete_one({'transaction_id': booking_id})
        if result.deleted_count == 0:
            result = repo.collection.delete_one({'booking_reference': booking_id})
            
        if result.deleted_count > 0:
            return Response({'message': 'Booking cancelled successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)

from django.shortcuts import render

class BookingReceiptView(APIView):
    def get(self, request, booking_id):
        try:
            repo = BookingRepository()
            flight_repo = FlightRepository()
            booking_doc = repo.collection.find_one({
                '$or': [
                    {'transaction_id': booking_id},
                    {'booking_reference': booking_id}
                ]
            })
            
            if not booking_doc:
                return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
                
            if '_id' in booking_doc:
                del booking_doc['_id']
                
            booking = Booking(**booking_doc)
            flight = None
            if booking.flight_id:
                flight = flight_repo.get_flight_by_id(booking.flight_id)
                
            return render(request, 'ticket.html', {
                'booking': booking, 
                'flight': flight,
                'pnr': booking.booking_reference
            })
            
        except Exception as e:
            print(f"Error generating receipt: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserStatsView(APIView):
    def get(self, request):
        email = request.query_params.get('email')
        if not email:
            return Response({'error': 'Email parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        booking_repo = BookingRepository()
        flight_repo = FlightRepository()
        
        bookings = booking_repo.get_by_user(email)
        
        total_flights = len(bookings)
        miles_earned = total_flights * 1250 # Simulated miles
        
        next_trip = None
        min_diff = float('inf')
        now = datetime.now()
        
        for booking in bookings:
            if booking.flight_id:
                flight = flight_repo.get_flight_by_id(booking.flight_id)
                if flight and flight.departure_time > now:
                    diff = (flight.departure_time - now).total_seconds()
                    if diff < min_diff:
                        min_diff = diff
                        next_trip = {
                            'destination': flight.destination,
                            'date': flight.departure_time,
                            'flight_number': flight.flight_number
                        }
        
        return Response({
            'total_flights': total_flights,
            'miles_earned': miles_earned,
            'next_trip': next_trip
        })
