from django.contrib.auth.signals import user_logged_in
from rest_framework.views import APIView
from user.models import User
from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from rest_framework_jwt.utils import jwt_payload_handler
import jwt
import json
from django.http import HttpResponse
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.decorators import api_view, permission_classes
from teleblog import settings
from .serializers import UserSerializer
from social.views import get_clearbit_data, get_emailhunter_data
from .auth import login
from teleblog.settings import *
from pymongo import MongoClient

client = MongoClient()
db = client[mongo_db_name]
mongo_users = db['users']


class Login(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        if not request.data or not request.data.get('email') or not request.data.get('password'):
            return Response({'Error': "Please provide email/password"}, status="400")

        email = request.data.get('email')
        users = User.objects.all().count()
        if users >= int(settings.number_of_users):
            return Response('Number of users more then limit', status=status.HTTP_403_FORBIDDEN)

        result_getting_info = {}
        serializer = UserSerializer(data=request.data)
        clearbit_data = get_clearbit_data(email)
        emailhunter_data = get_emailhunter_data(email)
        result_getting_info['clearbit'] = clearbit_data.get('data')
        result_getting_info['emailhunter'] = emailhunter_data.get('data')
        mongo_users.insert_one(result_getting_info)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'Error': "Invalid email/password"}, status="400")
        if user:
            jwt_token = login(user)
            user.token = jwt_token
            user.save()
            header = {"Authorization": f'Bearer {jwt_token}'}
            return Response(result_getting_info, status=status.HTTP_201_CREATED, headers=header)
        else:
            return Response(
                serializer.errors,
                status=400,
                content_type="application/json"
            )


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    # Allow only authenticated users to access this url
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        serializer = UserSerializer(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserList(APIView):
    """
    Get all userns
    """
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        snippets = User.objects.all()
        serializer = UserSerializer(snippets, many=True)
        return Response(serializer.data)

