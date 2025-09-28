from rest_framework import serializers
from .models import UserModel
from core.interfaces.usecase.criar_user_usecase import (
    CreateUserResponse,
    ChangeUserPasswordRequest,
    LoginUserRequest,
    LoginUserResponse
)

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = UserModel
        fields = ['id', 'email', 'password','first_name', 'last_name', 'is_superuser']
        read_only_fields = ['id','is_active', 'is_staff','is_superuser']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = UserModel(**validated_data)
        user.set_password(password)  
        user.save()
        return user
    
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

class UserAlterPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        write_only=True, required=True,  min_length=6, allow_blank=False
    )
    new_password = serializers.CharField(
        write_only=True, required=True,  min_length=6, allow_blank=False
    )
    
    def to_internal_value(self, data):
        return ChangeUserPasswordRequest(
            user_id=self.context['view'].kwargs['pk'],
            old_password=data.get("old_password"),
            new_password=data.get("new_password"),
        )
    
    
    def to_representation(self, instance):
        return {"sucess": instance.sucess}

class LoginRequestSerializer(serializers.Serializer):
    
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required= True)
    
    def validate(self, attrs: LoginUserRequest) -> LoginUserResponse:
        return  attrs

class LoginResponseSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)
    
    def to_representation(self, instance: LoginUserResponse):
        return {
            "id": instance.id,
            "email": instance.email,
            "access_token": instance.access_token,
            "refresh_token": instance.refresh_token,
        }
