from rest_framework import serializers
from .models import UserModel
from core.interfaces.usecase.criar_user_usecase import (
    CreateUserRequest,
    CreateUserResponse,
)

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = UserModel
        fields = ['id', 'email', 'password','first_name', 'last_name', 'is_superuser']
        read_only_fields = ['id','is_active', 'is_staff','is_superuser']

class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']
        read_only_fields = fields
        
    id = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name=serializers.CharField(read_only=True)
    is_active = serializers.CharField(read_only=True)
    is_staff = serializers.CharField(read_only=True)
    is_superuser = serializers.CharField(read_only=True)
    
    def to_representation(self, instance: CreateUserResponse):
        return {
            "id": instance.id,
            "email": instance.email,
            "first_name": instance.first_name,
            "last_name": instance.last_name,
            "is_active": instance.is_active,
            "is_staff": instance.is_staff,
            "is_superuser": instance.is_superuser
        }