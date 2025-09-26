from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
import uuid

from core.interfaces.usecase.criar_user_usecase import(
    CreateUserUseCase,
    ListUsersUseCase,
    GetUserByIdRequest,
    GetUserByIdUseCase,
    CreateUserRequest

)
from core.interfaces.usecase.criar_user_usecase import ListUsersRequest

from .repository import DjangoUserRepository
from .serializers import UserSerializer, UserReadSerializer
from .models import UserModel

class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = UserModel.objects.all()

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

class UserRetriveAPIView(generics.RetrieveAPIView):
    serializer_class = UserReadSerializer
    queryset = UserModel.objects.all()

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
