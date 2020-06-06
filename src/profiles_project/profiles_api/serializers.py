from rest_framework import serializers
from .models import UserProfile


class HelloSerializer(serializers.ModelSerializer):
    """Serializers a name field for testing our APIView."""
    class Meta:
        model = UserProfile
        fields = ['name']