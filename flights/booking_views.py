from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .repositories import BookingRepository
from .models import Booking
from datetime import datetime
import uuid

class BookingCreateView(APIView):
    def post(self, request):
        data = request.data
        user_email = data.get('user_email')
        flight_number = data.get('flight_number')
        passenger_details = data.get('passenger_details')
        
        if not user_email or not flight_number:
            return Response({'error': 'User email and flight number are required'}, status=status.HTTP_400_BAD_REQUEST)
            
        if not passenger_details or not isinstance(passenger_details, list) or len(passenger_details) == 0:
            return Response({'error': 'At least one passenger is required'}, status=status.HTTP_400_BAD_REQUEST)

        import random
        import string

        # Generate Transaction ID
        transaction_id = "TXN" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

        # Assign Seats
        for passenger in passenger_details:
            preference = passenger.get('seat_preference', 'Any')
            # Simple random seat assignment logic
            row = random.randint(1, 30)
            if preference == 'Window':
                col = random.choice(['A', 'F'])
            elif preference == 'Aisle':
                col = random.choice(['C', 'D'])
            else: # Middle or Any
                col = random.choice(['B', 'E'])
            
            passenger['seat_number'] = f"{row}{col}"

        booking = Booking(
            booking_reference=str(uuid.uuid4())[:8].upper(),
            transaction_id=transaction_id,
            user_email=user_email,
            flight_number=flight_number,
            booking_date=datetime.now(),
            passenger_details=passenger_details,
            status="CONFIRMED"
        )

        repo = BookingRepository()
        repo.create(booking)

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
        return Response([b.to_dict() for b in bookings])

class BookingCheckinView(APIView):
    def post(self, request):
        pnr = request.data.get('pnr')
        lastname = request.data.get('lastname')

        if not pnr or not lastname:
            return Response({'error': 'PNR and Last Name are required'}, status=status.HTTP_400_BAD_REQUEST)

        repo = BookingRepository()
        # Find booking by PNR (we need to implement get_by_pnr in repo or search)
        # Since we don't have get_by_pnr, we can search using find_one
        booking_doc = repo.collection.find_one({'booking_reference': pnr.upper()})
        
        if not booking_doc:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
        
        booking = Booking(**booking_doc)
        
        # Verify Last Name
        passenger_found = False
        for p in booking.passenger_details:
            # Assuming name is "First Last" or just "Last"
            # Simple check: is lastname in the full name (case insensitive)
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
        # In a real app, we would verify the user owns this booking
        # For now, we just delete it by transaction_id or booking_reference
        # But the URL param is likely the ID or Reference. 
        # Let's assume booking_id is the transaction_id or reference.
        
        # Try finding by transaction_id first
        result = repo.collection.delete_one({'transaction_id': booking_id})
        if result.deleted_count == 0:
            # Try by booking_reference
            result = repo.collection.delete_one({'booking_reference': booking_id})
            
        if result.deleted_count > 0:
            return Response({'message': 'Booking cancelled successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
