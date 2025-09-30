from rest_framework import serializers
from .models import UserModel
from core.interfaces.usecase.criar_user_usecase import (
    CreateUserResponse,
    ChangeUserPasswordRequest,
    LoginUserRequest,
    LoginUserResponse
)

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer responsável pela criação e validação de dados de usuários.

    Campos:
    - id: Identificador único do usuário (somente leitura).
    - email: Endereço de e-mail do usuário.
    - password: Senha do usuário (somente escrita, opcional).
    - first_name: Primeiro nome.
    - last_name: Sobrenome.
    - is_superuser: Indica se o usuário tem privilégios administrativos (somente leitura).

    Comportamento:
    - No método `create`, a senha é criptografada usando `set_password()` antes de salvar o usuário.
    - Campos como `is_active`, `is_staff` e `is_superuser` são protegidos contra escrita direta.
    """
    password = serializers.CharField(write_only=True, required=False)
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
    """
    Serializer utilizado para leitura dos dados de usuários.

    Campos:
    - id, email, first_name, last_name, is_active, is_staff, is_superuser: Todos são somente leitura.

    Comportamento:
    - O método `to_representation` transforma uma instância de `CreateUserResponse` em um dicionário serializado.
    - Ideal para retornar dados após criação ou consulta de usuários.
    """
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
    """
    Serializer responsável pela alteração de senha de um usuário.

    Campos:
    - old_password: Senha atual do usuário (obrigatória).
    - new_password: Nova senha desejada (obrigatória).

    Comportamento:
    - `to_internal_value`: Converte os dados recebidos em uma instância de `ChangeUserPasswordRequest`.
    - `to_representation`: Retorna o resultado da operação como um dicionário com chave `sucess`.
    """
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
    """
    Serializer utilizado para autenticação de usuários.

    Campos:
    - email: Endereço de e-mail do usuário (obrigatório).
    - password: Senha do usuário (obrigatória, somente escrita).

    Comportamento:
    - `validate`: Encapsula os dados em uma instância de `LoginUserRequest` para uso no caso de autenticação.
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required= True)
    
    def validate(self, attrs: LoginUserRequest) -> LoginUserResponse:
        return  attrs

class LoginResponseSerializer(serializers.Serializer):
    """
    Serializer utilizado para retornar os dados de autenticação bem-sucedida.

    Campos:
    - id: Identificador do usuário.
    - email: Endereço de e-mail.
    - access_token: Token de acesso gerado.
    - refresh_token: Token de atualização.

    Comportamento:
    - `to_representation`: Converte uma instância de `LoginUserResponse` em um dicionário serializado.
    - Ideal para resposta de login via OAuth2 ou JWT.
    """
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
