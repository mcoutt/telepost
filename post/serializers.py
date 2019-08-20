from rest_framework.validators import UniqueValidator, qs_exists
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import routers, serializers, viewsets, permissions
from django.contrib.auth.models import User
from user.models import User
from user.serializers import UserSerializer
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    created_date = serializers.ReadOnlyField()
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    user = UserSerializer(read_only=True)

    class Meta(object):
        model = Post
        fields = ('id', 'title', 'description', 'like',
                  'unlike', 'created_date', 'modified_date', 'user')
