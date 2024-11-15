# from django.contrib.auth.models import User
# from rest_framework import serializers
# from .models import UserProfile

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'password']
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         try:
#             user = User(**validated_data)
#             user.set_password(validated_data['password'])
#             user.save()
#             return user
#         except Exception as e:
#             raise serializers.ValidationError({"error": str(e)})
        
# class SetPinSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = ['pin']

# class ChangePinSerializer(serializers.ModelSerializer):
#     old_pin = serializers.CharField(required=True)
#     new_pin = serializers.CharField(required=True)

#     class Meta:
#         model = UserProfile
#         fields = ['old_pin', 'new_pin']



from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile
from .mongo_connection import get_mongo_client
import bcrypt

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'password']
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         try:
#             user = User(**validated_data)
#             user.set_password(validated_data['password'])
#             user.save()
#             # Create a UserProfile instance for the new user if needed
#             UserProfile.objects.create(user=user)  # Assuming a one-to-one relationship
#             return user
#         except Exception as e:
#             raise serializers.ValidationError({"error": str(e)})

class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Remove confirm_password from validated_data
        validated_data.pop('confirm_password', None)

        try:
            user = User(**validated_data)
            user.set_password(validated_data['password'])
            user.save()
            # Create a UserProfile instance for the new user if needed
            UserProfile.objects.create(user=user)  # Assuming a one-to-one relationship
            return user
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})

    def validate(self, data):
        if data['password'] != data.get('confirm_password'):
            raise serializers.ValidationError("Passwords do not match.")
        return data


class SetPinSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['pin']

    def update(self, instance, validated_data):
        # Hash the pin before saving
        pin = validated_data.get('pin')
        if pin:
            hashed_pin = bcrypt.hashpw(pin.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            instance.pin = hashed_pin
            instance.save()
        return instance

class ChangePinSerializer(serializers.Serializer):
    old_pin = serializers.CharField(required=True)
    new_pin = serializers.CharField(required=True)

    def validate_old_pin(self, value):
        user = self.context['request'].user
        client = get_mongo_client()
        db = client['ani']
        collection = db['user_profiles']
        
        # Retrieve the user profile from MongoDB
        profile = collection.find_one({"username": user.username})

        if not profile:
            raise serializers.ValidationError("User profile not found.")

        # Debugging output
        print("Retrieved stored pin:", profile['pin'])
        print("Provided old pin:", value)

        # Check if the old PIN matches
        if not bcrypt.checkpw(value.encode('utf-8'), profile['pin'].encode('utf-8')):
            raise serializers.ValidationError("Old PIN is incorrect.")
        
        return value

    def update(self, instance, validated_data):
        new_pin = validated_data.get('new_pin')
        if new_pin:
            # Hash the new pin before saving
            hashed_new_pin = bcrypt.hashpw(new_pin.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            # Update the pin in the MongoDB document
            client = get_mongo_client()
            db = client['ani']
            collection = db['user_profiles']
            # Use the username from the instance to find the correct document
            collection.update_one({"username": instance['username']}, {"$set": {"pin": hashed_new_pin}})
        return instance