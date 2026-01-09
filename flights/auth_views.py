import bcrypt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.db import get_users_collection, get_captchas_collection
from .utils import generate_captcha
import uuid
from datetime import datetime

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
        captcha_id = data.get('captcha_id')
        captcha_value = data.get('captcha_value')

        if not captcha_id or not captcha_value:
            return Response({'error': 'Captcha is required'}, status=status.HTTP_400_BAD_REQUEST)

        captchas = get_captchas_collection()
        stored = captchas.find_one({'captcha_id': captcha_id})
        
        if not stored or stored['text'] != captcha_value.upper():
            return Response({'error': 'Invalid Captcha'}, status=status.HTTP_400_BAD_REQUEST)
        
        captchas.delete_one({'captcha_id': captcha_id})

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

class ResendOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
            
        users = get_users_collection()
        user = users.find_one({'email': email})
        
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            
        import random
        otp = str(random.randint(100000, 999999))
        
        users.update_one({'email': email}, {'$set': {'otp': otp}})
        
        return Response({
            'message': 'OTP resent successfully',
            'debug_otp': otp
        }, status=status.HTTP_200_OK)

class UserUpdateView(APIView):
    def post(self, request):
        email = request.data.get('email')
        new_name = request.data.get('name')
        new_password = request.data.get('password')
        
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
            
        users = get_users_collection()
        user = users.find_one({'email': email})
        
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            
        update_fields = {}
        if new_name:
            update_fields['name'] = new_name
        if new_password:
            update_fields['password'] = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            
        if update_fields:
            users.update_one({'email': email}, {'$set': update_fields})
            
        updated_user = users.find_one({'email': email})
        
        return Response({
            'message': 'Profile updated successfully',
            'user': {
                'email': updated_user['email'],
                'name': updated_user['name'],
                'membership_id': updated_user.get('membership_id')
            }
        }, status=status.HTTP_200_OK)

class CaptchaView(APIView):
    def get(self, request):
        text = generate_captcha()
        captcha_id = str(uuid.uuid4())
        
        get_captchas_collection().insert_one({
            'captcha_id': captcha_id,
            'text': text,
            'created_at': datetime.now()
        })
        
        svg = f"""<svg width="150" height="50" xmlns="http://www.w3.org/2000/svg" style="border-radius: 4px;">
            <rect width="100%" height="100%" fill="#f1f5f9"/>
            <text x="50%" y="50%" font-family="monospace" font-size="24" font-weight="bold" fill="#334155" dominant-baseline="middle" text-anchor="middle" letter-spacing="4">{text}</text>
            <line x1="10" y1="10" x2="140" y2="40" stroke="#94a3b8" stroke-width="2" opacity="0.5"/>
            <line x1="10" y1="40" x2="140" y2="10" stroke="#94a3b8" stroke-width="2" opacity="0.5"/>
            <circle cx="20" cy="20" r="2" fill="#94a3b8" opacity="0.5"/>
            <circle cx="130" cy="30" r="2" fill="#94a3b8" opacity="0.5"/>
            <circle cx="70" cy="10" r="2" fill="#94a3b8" opacity="0.5"/>
        </svg>"""
        
        return Response({
            'captcha_id': captcha_id,
            'svg': svg
        })

class UserDeleteView(APIView):
    def delete(self, request):
        email = request.data.get('email')
        
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
            
        users = get_users_collection()
        result = users.delete_one({'email': email})
        
        if result.deleted_count == 0:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            
        return Response({'message': 'Account deleted successfully'}, status=status.HTTP_200_OK)
