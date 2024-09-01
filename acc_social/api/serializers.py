from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import *

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists() or  CustomUser.objects.filter(name=value).exists():
            raise serializers.ValidationError("Username/name already exists. Please choose a different one.")
        return value
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        token = Token.objects.create(user=user)
        return user,token

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    def validate(self, data):
        email = data.get('email').lower()
        password = data.get('password')

        user = authenticate(email=email, password=password)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid login credentials")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'name', 'username']


class FriendRequestsSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = FriendRequests
        fields = ['id', 'sender', 'receiver', 'is_accepted', 'created_at']

class FriendshipSerializer(serializers.ModelSerializer):
    friend = serializers.SerializerMethodField()

    class Meta:
        model = Friendships
        fields = ['friend', 'created_at']

    def get_friend(self, obj):
        request = self.context.get('request')
        user = request.user if request else None
        if obj.user1 == user:
            return UserSerializer(obj.user2).data
        return UserSerializer(obj.user1).data


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100