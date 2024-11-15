import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from bson import ObjectId 
from .mongo_connection import get_mongo_client

class MongoUser:
    def __init__(self, username, user_id):
        self.username = username
        self.id = user_id
    
    @property
    def is_authenticated(self):
        return True 

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = request.headers.get('Authorization', None)
        if not auth:
            return None
        try:
            prefix, token = auth.split()
            if prefix.lower() != 'bearer':
                raise AuthenticationFailed('Authorization header must start with Bearer')

            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            client = get_mongo_client()
            db = client['ani']
            collection = db['user_profiles']
            user_data = collection.find_one({"_id": ObjectId(payload['id'])})  # Assuming ObjectId is used
            if user_data is None:
                raise AuthenticationFailed('User not found')
            
            user = MongoUser(username=user_data['username'], user_id=str(user_data['_id']))
            return (user, None) 

        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
            raise AuthenticationFailed(str(e))
