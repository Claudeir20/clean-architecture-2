from core.domain.entities.user import User
from core.domain.repositories.user_repository import UserRepository
from dataclasses import dataclass
from core.interfaces.usecase.gateways import AuthGateway

@dataclass
class CreateUserRequest:
    id: str
    email: str
    first_name: str
    last_name: str
    password: str
    is_active: bool = True
    is_staff: bool = False
    is_superuser: bool = False


@dataclass
class CreateUserResponse:
    id: str
    email: str
    first_name: str
    last_name: str
    is_active: bool
    is_staff: bool
    is_superuser: bool 


class CreateUserUseCase:
    """
    Caso de uso responsável pela criação de um novo usuário no sistema.

    Recebe os dados necessários via CreateUserRequest, constrói a entidade de domínio User
    e delega ao repositório para persistência. Retorna os dados do usuário criado
    encapsulados em um CreateUserResponse.
    """
    def __init__(self, user_repositor: UserRepository):
        """
        Inicializa o caso de uso com a dependência do repositório de usuários.
        """
        self.user_repositor = user_repositor
    
    def execute(self, request: CreateUserRequest) -> CreateUserResponse:
        """
        Executa a criação de um novo usuário com base nos dados fornecidos.

        Args:
            request (CreateUserRequest): Dados do usuário a ser criado.

        Returns:
            CreateUserResponse: Dados do usuário criado.
        """
        user = User(
            email=request.email,
            first_name=request.first_name,
            last_name=request.last_name,
            is_active=request.is_active,
            is_staff=request.is_staff,
            is_superuser=request.is_superuser,
        )

        crated_user_response = self.user_repositor.create(user)
        
        return CreateUserResponse(
            id=crated_user_response.id,
            email=crated_user_response.email,
            first_name=crated_user_response.first_name,
            last_name=crated_user_response.last_name,
            is_active=crated_user_response.is_active,
            is_staff=crated_user_response.is_staff,
            is_superuser=crated_user_response.is_superuser
        )

@dataclass
class ListUsersRequest:
    offset: int = 0
    limit: int = 10
    search_query: str | None = None
    
@dataclass
class ListUsersResponse:
    users: list[CreateUserResponse]
    total_items: int
    offset: int
    limit: int


class ListUsersUseCase:
    """
    Caso de uso para listagem paginada e opcionalmente filtrada de usuários.

    Utiliza os parâmetros de paginação e busca contidos em ListUsersRequest
    e retorna uma ListUsersResponse com os dados dos usuários e metadados.
    """
    def __init__(self, user_repository: UserRepository):
        """
        Inicializa o caso de uso com a dependência do repositório de usuários.
        """
        self.user_repository = user_repository

    def execute(self, request: ListUsersRequest) -> ListUsersResponse:
        """
        Executa a listagem de usuários com base nos parâmetros fornecidos.

        Args:
            request (ListUsersRequest): Parâmetros de paginação e filtro.

        Returns:
            ListUsersResponse: Lista de usuários e metadados de paginação.
        """
        users_domain, total_items = self.user_repository.get_all_paginated_filtered(
            offset=request.offset,
            limit=request.limit,
            search_query=request.search_query
        )

        users_response = [
            CreateUserResponse(
                id=user.id,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                is_active=user.is_active,
                is_staff=user.is_staff,
                is_superuser=user.is_superuser
            )
            for user in users_domain
        ]

        return ListUsersResponse(
            users=users_response,
            total_items=total_items,
            offset=request.offset,
            limit=request.limit
        )

@dataclass
class GetUserByIdRequest:
    user_id: str

class GetUserByIdUseCase:
    """
    Caso de uso para buscar um usuário pelo seu identificador único.

    Recebe um GetUserByIdRequest com o ID do usuário e retorna os dados
    encapsulados em um CreateUserResponse.
    """
    def __init__(self, user_repository: UserRepository):
        """
        Inicializa o caso de uso com a dependência do repositório de usuários.
        """
        self.user_repository = user_repository
    
    def execute(self, request: GetUserByIdRequest) -> CreateUserResponse:
        user = self.user_repository.get_by_id(request.user_id)
        
        return CreateUserResponse(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active,
            is_staff=user.is_staff,
            is_superuser=user.is_superuser
        )

@dataclass
class GetUserByEmailRequest:
    user_email: str

class GetUserByEmailUseCase:
    """
    Caso de uso para buscar um usuário pelo seu e-mail.

    Recebe um GetUserByEmailRequest com o e-mail do usuário e retorna os dados
    encapsulados em um CreateUserResponse. Lança exceção se o usuário não for encontrado.
    """
    def __init__(self, user_repository: UserRepository):
        """
        Inicializa o caso de uso com a dependência do repositório de usuários.
        """
        self.user_repository = user_repository
    
    def execute(self, request: GetUserByEmailRequest) -> CreateUserResponse:
        """
        Executa a busca de um usuário pelo e-mail.

        Args:
            request (GetUserByEmailRequest): Contém o e-mail do usuário a ser buscado.

        Returns:
            CreateUserResponse: Dados do usuário encontrado.

        Raises:
            ValueError: Se nenhum usuário for encontrado com o e-mail fornecido.
        """
        user= self.user_repository.get_by_email(request.user_email)
        
        if not user:
            raise ValueError("Usuário não encontrado")
        
        return CreateUserResponse(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active,
            is_staff=user.is_staff,
            is_superuser=user.is_superuser
        )
@dataclass
class LoginUserRequest:
    email: str
    password: str

@dataclass
class LoginUserResponse:
    id: str
    email: str
    access_token: str
    refresh_token: str

class LoginUserUseCase:
    def __init__(self, user_repository: UserRepository, auth_gateway: AuthGateway):
        self.user_repository = user_repository
        self.auth_gateway = auth_gateway
    
    def execute(self, request: LoginUserRequest) -> LoginUserResponse:
        user = self.user_repository.get_by_email(request.email)
        
        if not user:
            raise ValueError("Credenciais inválidas")

        if not self.auth_gateway.check_password(user.id, request.password):
            raise ValueError("Credenciais inválidas")
        
        access_token, refresh_token = self.auth_gateway.create_tokens(user.id)
        
        return LoginUserResponse(
            id=user.id,
            email=user.email,
            access_token=access_token,
            refresh_token=refresh_token
        )
        
@dataclass
class ChangeUserPasswordRequest:
    user_id: str
    old_password: str
    new_password: str

@dataclass
class ChageUserPasswordResponse:
    sucess: bool

class ChageUserPasswordUseCase:
    def __init__(self, user_repository: UserRepository, auth_gateway: AuthGateway):
        self.user_repository = user_repository
        self.auth_gateway = auth_gateway
    
    def execute(self, request: ChangeUserPasswordRequest) -> ChageUserPasswordResponse:
        if not self.auth_gateway.check_password(request.user_id, request.old_password):
            raise ValueError("Senha antiga estar incorreta")
        
        user = self.user_repository.get_by_id(request.user_id)
        if not user:
            raise ValueError("Usuário não encontrado")
        self.auth_gateway.set_password(user.id, request.new_password)
        return ChageUserPasswordResponse(sucess=True)