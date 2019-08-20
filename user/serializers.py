from rest_framework import serializers
from rest_framework.validators import UniqueValidator, qs_exists
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField()

    def create(self, validated_data):
        user = User(email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta(object):
        model = User
        fields = ('id', 'email', 'fname', 'lname',
                  'date_joined', 'password', 'post_count')
        # extra_kwargs = {'password': {'write_only': True}}
