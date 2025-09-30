from .serializers import LoginRequestSerializer, LoginResponseSerializer
from core.interfaces.usecase.criar_user_usecase import(
    LoginUserRequest,
    LoginUserUseCase
)
from .repository import DjangoUserRepository
from .auth_gateway_dj import DjangoAuthGateway
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

class LoginAPIView(APIView):
    """
    API view responsável por autenticar usuários e retornar tokens de acesso.

    Método:
    - POST: Recebe credenciais de login (e-mail e senha) e retorna tokens de autenticação.

    Permissões:
    - Acesso liberado para qualquer usuário (AllowAny), inclusive não autenticado.

    Fluxo:
    1. Valida os dados recebidos via `LoginRequestSerializer`.
    2. Cria uma instância de `LoginUserRequest` com e-mail e senha.
    3. Executa o caso de uso `LoginUserUseCase`, que:
    - Verifica se o usuário existe.
    - Valida a senha.
    - Gera tokens de acesso e refresh via `DjangoAuthGateway`.
    4. Serializa a resposta com `LoginResponseSerializer`.
    5. Retorna os tokens e dados do usuário autenticado.

    Tratamento de erros:
    - Se as credenciais forem inválidas, retorna HTTP 401 com mensagem de erro.
    """
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = LoginRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        login_request = LoginUserRequest(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        user_repository = DjangoUserRepository()
        auth_gateway = DjangoAuthGateway()
        use_case = LoginUserUseCase(user_repository, auth_gateway)

        try:
            response_data = use_case.execute(login_request)
            response_serializer = LoginResponseSerializer(response_data)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)