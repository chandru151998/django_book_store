from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User


class RegistrationSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'phone_no', 'location']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['id']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)

    def create(self, validated_data):
        user = authenticate(**validated_data)
        if not user:
            raise Exception('Invalid credentials')
        return user
