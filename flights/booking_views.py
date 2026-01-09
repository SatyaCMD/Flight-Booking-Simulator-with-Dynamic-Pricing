from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .repositories import BookingRepository, FlightRepository
from .models import Booking
from core.db import get_captchas_collection
from datetime import datetime
import uuid
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import random
import string
from io import BytesIO

class BookingCreateView(APIView):
    def post(self, request):
        data = request.data
        user_email = data.get('user_email')
        flight_number = data.get('flight_number')
        flight_id = data.get('flight_id')
        passenger_details = data.get('passenger_details')
        travel_class = data.get('travel_class', 'Economy')
        payment_method = data.get('payment_method', 'Card')
        payment_details = data.get('payment_details', '')
        captcha_id = data.get('captcha_id')
        captcha_value = data.get('captcha_value')

        if not captcha_id or not captcha_value:
            return Response({'error': 'Captcha is required for payment'}, status=status.HTTP_400_BAD_REQUEST)

        captchas = get_captchas_collection()
        stored = captchas.find_one({'captcha_id': captcha_id})
        
        if not stored or stored['text'] != captcha_value.upper():
            return Response({'error': 'Invalid Captcha'}, status=status.HTTP_400_BAD_REQUEST)
        
        captchas.delete_one({'captcha_id': captcha_id})
        
        if not user_email or not flight_number:
            return Response({'error': 'User email and flight number are required'}, status=status.HTTP_400_BAD_REQUEST)
            
        if not passenger_details or not isinstance(passenger_details, list) or len(passenger_details) == 0:
            return Response({'error': 'At least one passenger is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate Payment Details
        if payment_method == 'upi':
            if not payment_details or '@' not in payment_details:
                return Response({'error': 'Invalid UPI ID'}, status=status.HTTP_400_BAD_REQUEST)
        elif payment_method == 'netbanking':
            if not payment_details:
                return Response({'error': 'Bank selection is required for Net Banking'}, status=status.HTTP_400_BAD_REQUEST)
        elif payment_method == 'card':
             if not payment_details or len(payment_details) < 4:
                 # In a real app we would validate the card token/details more thoroughly
                 pass

        flight_repo = FlightRepository()
        flight = flight_repo.get_flight_by_id(flight_id)

        if not flight:
            return Response({'error': 'Flight not found'}, status=status.HTTP_404_NOT_FOUND)

        for passenger in passenger_details:
            seat_number = passenger.get('seat_number')
            if not seat_number:
                return Response({'error': 'Seat number is required for each passenger'}, status=status.HTTP_400_BAD_REQUEST)

            row_num_str = ''.join(filter(str.isdigit, seat_number))
            if not row_num_str:
                return Response({'error': f'Invalid seat number: {seat_number}'}, status=status.HTTP_400_BAD_REQUEST)
                
            row_num = int(row_num_str)
            col_char = ''.join(filter(str.isalpha, seat_number)).upper()
            
            if not col_char or row_num <= 0 or row_num > len(flight.seat_map):
                return Response({'error': f'Invalid seat number: {seat_number}'}, status=status.HTTP_400_BAD_REQUEST)

            col_index = ord(col_char) - ord('A')
            aisle_offset = 0
            for i in range(len(flight.seat_map[row_num - 1])):
                if flight.seat_map[row_num - 1][i] == 'X' and i <= col_index:
                    aisle_offset += 1
            
            actual_col_index = col_index + aisle_offset

            if actual_col_index >= len(flight.seat_map[row_num - 1]) or flight.seat_map[row_num - 1][actual_col_index] != 'A':
                return Response({'error': f'Seat {seat_number} is not available'}, status=status.HTTP_400_BAD_REQUEST)
            
            row_list = list(flight.seat_map[row_num - 1])
            row_list[actual_col_index] = 'U'
            flight.seat_map[row_num - 1] = "".join(row_list)


        transaction_id = "TXN" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        flight_repo.update_flight(flight)

        booking = Booking(
            booking_reference=str(uuid.uuid4())[:8].upper(),
            transaction_id=transaction_id,
            user_email=user_email,
            flight_number=flight_number,
            booking_date=datetime.now(),
            passenger_details=passenger_details,
            flight_id=flight_id,
            origin=flight.origin,
            destination=flight.destination,
            travel_class=travel_class,
            payment_method=payment_method,
            payment_details=payment_details,
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
                is_fallback = False
                
                if not flight and booking.flight_number:
                    flight = flight_repo.get_flight_by_number(booking.flight_number)
                    is_fallback = True
                
                if flight:
                    details = {
                        'origin': flight.origin,
                        'destination': flight.destination,
                        'airline_code': flight.airline_code
                    }
                    if not is_fallback:
                        details['departure_time'] = flight.departure_time
                        details['arrival_time'] = flight.arrival_time
                        
                    b_dict['flight_details'] = details
            
            if 'flight_details' not in b_dict:
                 b_dict['flight_details'] = {}

            if 'origin' not in b_dict['flight_details'] and booking.origin:
                b_dict['flight_details']['origin'] = booking.origin
            
            if 'destination' not in b_dict['flight_details'] and booking.destination:
                b_dict['flight_details']['destination'] = booking.destination
            results.append(b_dict)
        return Response(results)

class BookingCheckinView(APIView):
    def post(self, request):
        pnr = request.data.get('pnr')

        if not pnr:
            return Response({'error': 'PNR is required'}, status=status.HTTP_400_BAD_REQUEST)

        repo = BookingRepository()
        booking_doc = repo.collection.find_one({'booking_reference': pnr.upper()})
        
        if not booking_doc:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if '_id' in booking_doc:
            del booking_doc['_id']
            
        booking = Booking(**booking_doc)
        
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

from datetime import timedelta
import random

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
                if not flight and booking.flight_number:
                    flight = flight_repo.get_flight_by_number(booking.flight_number)
            
            gate_letter = random.choice(['A', 'B', 'C', 'D', 'E', 'F'])
            gate_number = random.randint(1, 12)
            gate = f"{gate_letter}{gate_number}" 
            boarding_time = None
            if flight and flight.departure_time:
                boarding_time = flight.departure_time - timedelta(minutes=45)
                
            return render(request, 'ticket.html', {
                'booking': booking, 
                'flight': flight,
                'pnr': booking.booking_reference,
                'gate': gate,
                'boarding_time': boarding_time
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
        miles_earned = total_flights * 1250 
        
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

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO

class BookingDownloadReceiptView(APIView):
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
                if not flight and booking.flight_number:
                    flight = flight_repo.get_flight_by_number(booking.flight_number)

            taxes = 45.00
            base_price = flight.base_price if flight else 0
            num_passengers = len(booking.passenger_details) if booking.passenger_details else 1
            total_price = (base_price * num_passengers) + taxes

            return render(request, 'receipt.html', {
                'booking': booking, 
                'flight': flight,
                'taxes': taxes,
                'total_price': total_price,
                'payment_method': f"{booking.payment_method} ({booking.payment_details})" if booking.payment_details else booking.payment_method
            })
            
        except Exception as e:
            print(f"Error generating receipt: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
