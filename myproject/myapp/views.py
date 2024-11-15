# # myapp/views.py

# from django.contrib.auth import authenticate
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.tokens import RefreshToken
# from .serializers import UserSerializer, SetPinSerializer, ChangePinSerializer
# from .models import UserProfile 
# from bson import ObjectId
# from .mongo_connection import get_mongo_client
# from django.http import JsonResponse
# import bcrypt

# class SignupView(APIView):
#     def post(self, request):
#         # Get the MongoDB client
#         client = get_mongo_client()
#         db = client['ani']  # Use your database name
#         collection = db['user_profiles']  # Replace with your actual collection name

#         # Extract user data from the request
#         username = request.data.get('username')
#         password = request.data.get('password')

#         # Hash the password for security
#         hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

#         # Create a new user profile
#         user_data = {
#             "username": username,
#             "password": hashed_password.decode('utf-8'),  # Store the hashed password as a string
#         }

#         # Insert the user data into the collection
#         result = collection.insert_one(user_data)

#         # Prepare the response data
#         user_data_response = {
#             "id": str(result.inserted_id),  # Convert ObjectId to string
#             "username": username
#         }

#         return JsonResponse(user_data_response, status=201)
    
# class LoginView(APIView):
#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         user = authenticate(username=username, password=password)
#         if user:
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#             })
#         return Response({"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# class DashboardView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         return Response({"message": "Welcome to the dashboard!"})

# class SetPinView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#            # Try to get the UserProfile, create one if it doesn't exist
#            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
#            serializer = SetPinSerializer(user_profile, data=request.data)
#            if serializer.is_valid():
#                serializer.save()
#                return Response({"message": "PIN set successfully."}, status=status.HTTP_200_OK)
#            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class ChangePinView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         user_profile = UserProfile.objects.get(user=request.user)
#         serializer = ChangePinSerializer(data=request.data)
#         if serializer.is_valid():
#             if user_profile.pin != serializer.validated_data['old_pin']:
#                 return Response({"error": "Old PIN is incorrect."}, status=status.HTTP_400_BAD_REQUEST)
#             user_profile.pin = serializer.validated_data['new_pin']
#             user_profile.save()
#             return Response({"message": "PIN changed successfully."}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class FetchDataView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         client = get_mongo_client()  # Get the MongoDB client
#         db = client['ani']  # Use the database name 'ani'
#         collection = db['your_collection_name']  # Replace with your actual collection name

#         # Example: Fetch all documents from the collection
#         documents = list(collection.find({}))
        
#         # Convert ObjectId to string for JSON serialization
#         for doc in documents:
#             doc['_id'] = str(doc['_id'])  # Convert ObjectId to string

#         return Response(documents, status=status.HTTP_200_OK)







from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response
from .models import UserProfile 
from .serializers import UserSerializer, SetPinSerializer, ChangePinSerializer
from .mongo_connection import get_mongo_client
from .mongo_connection import get_blacklist_collection
import bcrypt
import jwt
import datetime
from django.conf import settings
from django.core.mail import send_mail

class SignupView(APIView):
    def post(self, request):
        client = get_mongo_client()
        db = client['ani']
        collection = db['user_profiles']

        username = request.data.get('username')
        email = request.data.get('email')  # Get the email from the request
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        if collection.find_one({"username": username}):
            return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate that the passwords match
        if password != confirm_password:
            return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Create the user data without the PIN
        user_data = {
            "username": username,
            "email": email,
            "password": hashed_password.decode('utf-8'),
            # No PIN is set during signup
        }

        result = collection.insert_one(user_data)

        user_data_response = {
            "id": str(result.inserted_id),
            "username": username,
            "email": email
        }

        return Response(user_data_response, status=status.HTTP_201_CREATED)



class LoginView(APIView):
    def post(self, request):
        client = get_mongo_client()
        db = client['ani']
        collection = db['user_profiles']

        username = request.data.get('username')
        password = request.data.get('password')

        user = collection.find_one({"username": username})

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            user_id = str(user['_id'])
            payload = {
                'username': username,
                'id': user_id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            }

            # Generate token using PyJWT
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

            return JsonResponse({
                'token': token,
            }, status=200)

        return JsonResponse({"error": "Invalid Credentials"}, status=401)


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Your existing logic
            return JsonResponse({"message": "Welcome to the dashboard!"})

        except AuthenticationFailed as e:
            # Catch the AuthenticationFailed exception raised by the middleware
            return JsonResponse({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        
        except Exception as e:
            # Generic error handler
            return JsonResponse({"error": "Something went wrong. Please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Extract the token from the Authorization header
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        else:
            return Response({"error": "Token not provided."}, status=400)

        try:
            # Decode the token to ensure it's valid
            jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response({"error": "Token has already expired."}, status=400)
        except jwt.InvalidTokenError:
            return Response({"error": "Invalid token."}, status=400)

        # Save the token in the blacklist collection
        client = get_mongo_client()
        db = client['ani']
        blacklist_collection = get_blacklist_collection()
        blacklist_collection.insert_one({"token": token})

        return Response({"message": "Logged out successfully."}, status=200)


class SetPinView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        client = get_mongo_client()
        db = client['ani']
        collection = db['user_profiles']

        user = request.user  # Get the user from the request
        user_profile = collection.find_one({"username": user.username})

        if not user_profile:
            return Response({"error": "User profile not found."}, status=404)

        # Check if the PIN is already set
        if 'pin' in user_profile and user_profile['pin'] is not None:
            return Response({"error": "PIN is already set."}, status=400)

        # Use the serializer to validate and update the PIN
        pin = request.data.get('pin')
        if pin:
            # Hash the new PIN and update the existing user record
            hashed_pin = bcrypt.hashpw(pin.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            collection.update_one({"_id": user_profile['_id']}, {"$set": {"pin": hashed_pin}})
            return Response({"message": "PIN set successfully."}, status=200)

        return Response({"error": "PIN is required."}, status=400)

class ChangePinView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user  # Get the authenticated user
        old_pin = request.data.get('old_pin')
        new_pin = request.data.get('new_pin')

        if not old_pin or not new_pin:
            return Response({"error": "Both old and new PIN are required."}, status=400)

        client = get_mongo_client()
        db = client['ani']
        collection = db['user_profiles']
        user_profile = collection.find_one({"username": user.username})

        if not user_profile:
            return Response({"error": "User profile not found."}, status=404)

        # Verify the old PIN
        if 'pin' not in user_profile or user_profile['pin'] is None:
            return Response({"error": "No PIN has been set."}, status=400)

        if not bcrypt.checkpw(old_pin.encode('utf-8'), user_profile['pin'].encode('utf-8')):
            return Response({"error": "Old PIN is incorrect."}, status=400)

        # Hash the new PIN and update
        hashed_new_pin = bcrypt.hashpw(new_pin.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        collection.update_one({"_id": user_profile['_id']}, {"$set": {"pin": hashed_new_pin}})

        return Response({"message": "PIN changed successfully."}, status=200)
    

class UnlockView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user  # Get the authenticated user
        pin = request.data.get('pin')

        if not pin:
            return Response({"error": "PIN is required."}, status=400)

        client = get_mongo_client()
        db = client['ani']
        collection = db['user_profiles']
        user_profile = collection.find_one({"username": user.username})

        if not user_profile:
            return Response({"error": "User profile not found."}, status=404)

        # Check if the PIN is set and if it matches
        if 'pin' in user_profile and user_profile['pin'] is not None:
            if bcrypt.checkpw(pin.encode('utf-8'), user_profile['pin'].encode('utf-8')):
                return Response({"message": "Door unlocked."}, status=200)
            else:
                return Response({"error": "Unlock error: Incorrect PIN."}, status=400)
        else:
            return Response({"error": "No PIN has been set."}, status=400)
        

class RequestPasswordResetView(APIView):
    def post(self, request):
        client = get_mongo_client()
        db = client['ani']
        collection = db['user_profiles']

        email = request.data.get('email')
        user = collection.find_one({"email": email})

        if not user:
            return Response({"error": "No user found with this email."}, status=status.HTTP_404_NOT_FOUND)

        # Create a password reset token
        payload = {
            'email': email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),  # Token valid for 1 hour
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        # Send email with password reset link (for demonstration, we will print the link)
        # reset_link = f"http://127.0.0.1:8000/api/reset-password/{token}/"
        reset_link = f"http://localhost:3000/reset-password/{token}"

        send_mail(
            subject='Password Reset Request',
            message=f'You can reset your password using the following link: {reset_link}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )

        return Response({"message": "Password reset link has been sent."}, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    def post(self, request, token):
        client = get_mongo_client()
        db = client['ani']
        collection = db['user_profiles']

        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        # Validate that the passwords match
        if password != confirm_password:
            return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Decode the token
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            email = payload['email']
        except jwt.ExpiredSignatureError:
            return Response({"error": "The reset link has expired."}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.InvalidTokenError:
            return Response({"error": "Invalid reset link."}, status=status.HTTP_400_BAD_REQUEST)

        # Hash the new password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Update the user's password in the database
        collection.update_one({"email": email}, {"$set": {"password": hashed_password}})

        return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
    

class FetchDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        client = get_mongo_client()
        db = client['ani']
        collection = db['user_profiles']

        user_profile = collection.find_one({"username": request.user.username})
        if user_profile:
            user_profile['_id'] = str(user_profile['_id'])  # Convert ObjectId to string for JSON response
            return JsonResponse(user_profile, status=200)
        return JsonResponse({"error": "User profile not found."}, status=404)