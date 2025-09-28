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

class LoginAPIView(APIView):
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