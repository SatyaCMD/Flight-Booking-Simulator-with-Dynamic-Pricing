import bcrypt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.db import get_users_collection

class SignupView(APIView):
    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')

        if not email or not password or not name:
            return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        users = get_users_collection()
        if users.find_one({'email': email}):
            return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        import random
        membership_id = f"MEM{random.randint(10000, 99999)}"

        user = {
            'email': email,
            'password': hashed_password, 
            'name': name,
            'membership_id': membership_id
        }
        users.insert_one(user)

        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        users = get_users_collection()
        user = users.find_one({'email': email})

        if not user:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if bcrypt.checkpw(password.encode('utf-8'), user['password']):
            import random
            otp = str(random.randint(100000, 999999))
            users.update_one({'email': email}, {'$set': {'otp': otp}})
            
            return Response({
                'message': 'OTP sent',
                'status': 'OTP_REQUIRED',
                'email': email,
                'debug_otp': otp  
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class VerifyOTPView(APIView):
    def post(self, request):
        data = request.data
        email = data.get('email')
        otp = data.get('otp')

        if not email or not otp:
            return Response({'error': 'Email and OTP are required'}, status=status.HTTP_400_BAD_REQUEST)

        users = get_users_collection()
        user = users.find_one({'email': email})

        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if user.get('otp') == otp:
            update_data = {'$unset': {'otp': ""}}
            membership_id = user.get('membership_id')
            if not membership_id:
                import random
                membership_id = f"MEM{random.randint(10000, 99999)}"
                update_data['$set'] = {'membership_id': membership_id}
            
            users.update_one({'email': email}, update_data)
            
            return Response({
                'message': 'Login successful',
                'user': {
                    'email': user['email'],
                    'name': user['name'],
                    'membership_id': membership_id
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

