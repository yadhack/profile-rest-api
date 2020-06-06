from rest_framework import serializers
from .models import UserProfile
from . import models


class UserProfileSerializer(serializers.ModelSerializer):
    """A serializer for our user profile objects."""

    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class HelloSerializer(serializers.ModelSerializer):
    """Serializers a name field for testing our APIView."""

    class Meta:
        model = UserProfile
        fields = ['name']

    def create(self, validated_data):
        """Create and return a new user."""

        user = models.UserProfile(
            email=validated_data['email'],
            name=validated_data['name'],
        )
        user.set_password(validated_data['password'])

        user.save()

        return user


class ProfileFeedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProfileFeedItem
        fields = ('id', 'user_profile', 'status_text', 'created_on')
        extra_kwargs = {'user_profile': {'read_only': True}}
