import jwt
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from .mongo_connection import get_mongo_client

class BlacklistTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]

            # Check if the token is blacklisted
            client = get_mongo_client()
            db = client['ani']
            blacklist_collection = db['blacklisted_tokens']
            
            if blacklist_collection.find_one({"token": token}):
                raise AuthenticationFailed("This token has been blacklisted. Please log in again.")

            try:
                jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed("Token has expired.")
            except jwt.InvalidTokenError:
                raise AuthenticationFailed("Invalid token.")

        response = self.get_response(request)
        return response
