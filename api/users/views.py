import uuid
from rest_framework import generics, status
from rest_framework.response import Response
from .repository import DjangoUserRepository
from .serializers import UserSerializer, UserReadSerializer
from rest_framework.permissions import IsAdminUser
from core.domain.entities.user import User
from .models import UserModel
from core.interfaces.usecase.criar_user_usecase import(
    CreateUserUseCase,
    ListUsersUseCase,
    GetUserByIdRequest,
    GetUserByIdUseCase,
    CreateUserRequest,
    ListUsersRequest
)


class UserListCreateAPIView(generics.ListCreateAPIView):
    """
    API view responsável por listar usuários e criar novos registros.

    Métodos:
    - GET: Retorna uma lista paginada dos usuários cadastrados no sistema.
    - POST: Cria um novo usuário com os dados fornecidos no corpo da requisição.

    Permissões:
    - Apenas usuários administradores (IsAdminUser) podem acessar esta view.

    Serializers:
    - POST utiliza o `UserSerializer` para validação e criação.
    - GET utiliza o `UserReadSerializer` para leitura dos dados.

    Regras de negócio:
    - A criação de usuário é delegada ao caso de uso `CreateUserUseCase`.
    - A listagem é feita via `ListUsersUseCase`, com paginação fixa (offset=0, limit=10).
    """
    queryset = UserModel.objects.all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return UserSerializer
        return UserReadSerializer

    def get(self, request):
        repo = DjangoUserRepository()
        use_case = ListUsersUseCase(repo)

        request_data = ListUsersRequest(offset=0, limit=10)
        response_data = use_case.execute(request_data)

        serializer = self.get_serializer(response_data.users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        repo = DjangoUserRepository()
        use_case = CreateUserUseCase(repo)

        request_data = CreateUserRequest(
            id=str(uuid.uuid4()),
            email=serializer.validated_data['email'],
            first_name=serializer.validated_data['first_name'],
            last_name=serializer.validated_data['last_name'],
            is_active=True,
            is_staff=False,
            password=serializer.validated_data['password']
        )

        user = use_case.execute(request_data)
        response_serializer = UserReadSerializer(user)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class RetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view responsável por recuperar, atualizar ou excluir um usuário específico.

    Métodos:
    - GET (retrieve): Retorna os dados de um usuário com base no ID fornecido.
    - PATCH/PUT (update): Atualiza os dados do usuário, exceto a senha.
    - DELETE (destroy): Remove o usuário do sistema.

    Permissões:
    - Apenas usuários administradores (IsAdminUser) podem acessar esta view.

    Serializers:
    - Utiliza `UserSerializer` para entrada de dados.
    - Utiliza `UserReadSerializer` para saída de dados.

    Regras de negócio:
    - A recuperação é feita via `GetUserByIdUseCase`.
    - A atualização preserva a senha atual e delega ao repositório `DjangoUserRepository`.
    - A exclusão é feita diretamente via model (herança DRF).
    """
    
    serializer_class = UserSerializer
    queryset = UserModel.objects.all()
    permission_classes = [IsAdminUser]

    def retrieve(self, request, *args, **kwargs):
        user_id = kwargs['pk']
        get_user_request = GetUserByIdRequest(user_id=str(user_id))

        repo = DjangoUserRepository()
        get_user_use_case = GetUserByIdUseCase(repo)

        try:
            user_response = get_user_use_case.execute(get_user_request)
            response_serializer = UserReadSerializer(instance=user_response)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
    
    def update(self, request, *args, **kwargs):
        user_id = kwargs['pk']

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        repo = DjangoUserRepository()

    # Busca o usuário atual
        get_user_use_case = GetUserByIdUseCase(repo)
        existing_user = get_user_use_case.execute(GetUserByIdRequest(user_id=user_id))

    # Atualiza os dados
        updated_user = User(
            id=existing_user.id,
            email=serializer.validated_data['email'],
            first_name=serializer.validated_data['first_name'],
            last_name=serializer.validated_data['last_name'],
            is_active=existing_user.is_active,
            is_staff=existing_user.is_staff,
            is_superuser=existing_user.is_superuser
        )

        updated_user = repo.update(updated_user)

        response_serializer = UserReadSerializer(updated_user)
        return Response(response_serializer.data, status=status.HTTP_200_OK)