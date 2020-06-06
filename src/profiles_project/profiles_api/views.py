from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import HelloSerializer, UserProfileSerializer,ProfileFeedItemSerializer
from . import models
from . import permission
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handles craeting, creating and updating profiles."""

    serializer_class = UserProfileSerializer

    queryset = models.UserProfile.object.all()

    authentication_classes = (TokenAuthentication,)
    permission_classes = (permission.UpdateOwnProfile,IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)


class LoginViewSet(viewsets.ViewSet):
    """Checks email and password and return auth token."""
    serializer_class = AuthTokenSerializer

    def create(self, request):
        """Use the obtainAuthtoken APIView to validate and create a token."""

        return ObtainAuthToken().post(request)


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed items."""

    authentication_classes = (TokenAuthentication,)
    serializer_class = ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (permission.PostOwnStatus, IsAuthenticatedOrReadOnly)

    def perform_create(self, serializer):
        """"set the user profile to the logged in user."""
        serializer.save(user_profile=self.request.user)


class HelloApiView(APIView):
    """Test API view."""
    serializer_class = HelloSerializer

    def get(self, request, format=None):
        """Return a list of APIView features."""

        an_apiview = [
            'Uses HTTP methods as function (get, post, patch, put, delete).',
            'It is similar to a traditional Django view.',
            'Gives you the most control over your logic.',
            'Is mapped manually to URLs'
        ]

        return Response({'message': 'Hello!', 'an_apiview': an_apiview})

    def post(self, request):

        """Create a hello message with our name."""

        serializer = HelloSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Handles updating and object."""

        return Response({"method": 'put'})

    def patch(self, request, pk=None):
        """Patch request, only updates fields provided in the request."""

        return Response({'method': 'patch'})

    def delete(self, request, pk=None):
        """Deletes and object."""

        return Response({'method': 'delete'})


class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet."""

    serializer_class = HelloSerializer

    def list(self, request):
        """Return a hello message."""

        a_viewset = [
            'Uses action (list, create, retrieve, update, partial_update)',
            'Automatically maps to URLs using routers.',
            'Provides more functionality with less code'
        ]
        return Response({'message': 'Hello!', 'a_viewset': a_viewset})

    def create(self, request):
        """Create a new hello message."""

        serializer = HelloSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handles getting an object by its ID."""

        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        """Handles updating an objects."""

        return Response({'http_method': 'UPDATE'})

    def partial_update(self, request, pk=None):
        """Handles updating part of an objects."""

        return Response({'http_method': 'Patch'})

    def destroy(self, request, pk=None):
        """Handles removing an object."""

        return Response({'http_method': 'DELETE'})
