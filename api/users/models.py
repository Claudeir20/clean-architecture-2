from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid
from core.domain.entities.user import User as DomainUser
# Create your models here.

class UserManager(BaseUserManager):
    """
    Gerenciador personalizado para o modelo de usuário.

    Responsável por criar usuários comuns e superusuários, garantindo
    a normalização do e-mail e a aplicação da criptografia de senha.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Cria e retorna um usuário com o e-mail e senha fornecidos.

        Parâmetros:
        - email (str): Endereço de e-mail do usuário.
        - password (str): Senha em texto plano (será criptografada).
        - extra_fields (dict): Campos adicionais como nome, sobrenome, etc.

        Retorna:
        - UserModel: Instância do usuário criado.

        Levanta:
        - ValueError: Se o e-mail não for fornecido.
        """
        if not email:
            raise ValueError("Email é obrigatrio")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        """
        Cria e retorna um superusuário com permissões administrativas.

        Parâmetros:
        - email (str): Endereço de e-mail do superusuário.
        - password (str): Senha em texto plano.
        - extra_fields (dict): Campos adicionais.

        Retorna:
        - UserModel: Instância do superusuário criado.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)
    
    
    
class UserModel(AbstractBaseUser, PermissionsMixin):
    """
    Modelo de usuário personalizado baseado em AbstractBaseUser.

    Representa os dados persistidos no banco de dados e integra com
    o sistema de autenticação do Django.

    Campos:
    - id (UUID): Identificador único do usuário.
    - email (str): Endereço de e-mail (usado como login).
    - first_name (str): Primeiro nome.
    - last_name (str): Sobrenome.
    - is_active (bool): Indica se o usuário está ativo.
    - is_staff (bool): Indica se o usuário tem acesso ao admin.
    - is_superuser (bool): Indica se o usuário tem permissões totais.

    Configurações:
    - USERNAME_FIELD: Campo usado para login (email).
    - REQUIRED_FIELDS: Campos obrigatórios além do email.
    - objects: Usa o gerenciador personalizado `UserManager`.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)  # Isso define um campo, não um valor

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def to_domain(self) -> DomainUser:
        """
        Converte o modelo de banco de dados em uma entidade de domínio.

        Retorna:
        - DomainUser: Instância da entidade de domínio `User`.
        """
        return DomainUser(
            id=str(self.id),
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            password=self.password,
            is_active=self.is_active,
            is_staff=self.is_staff,
            is_superuser=self.is_superuser
        )

    def __str__(self):
        """
        Retorna a representação textual do usuário.

        Retorna:
        - str: O e-mail do usuário.
        """
        return self.email
    
    class Meta:
        """
        Metadados do modelo.

        Define nomes legíveis para o Django Admin.
        """
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
