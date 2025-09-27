from core.domain.entities.user import User
from core.domain.repositories.user_repository import UserRepository
from api.users.models import UserModel
from django.db.models import Q

class DjangoUserRepository(UserRepository):
    def create(self, user: User) -> User:
        if UserModel.objects.filter(email=user.email).exists():
            raise ValueError("Email já está em uso")

        model = UserModel.objects.create(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active,
            is_staff=user.is_staff,
            is_superuser=user.is_superuser
        )
        model.set_password("default_password") 
        model.save()
        return model.to_domain()

    def get_all(self) -> list[User]:
        return [user_model.to_domain() for user_model in UserModel.objects.all()]

    
    def get_by_id(self, user_id: str) -> User:
        try:
            user_model = UserModel.objects.get(id=user_id)
            return user_model.to_domain()
        except:
            raise ValueError("Usuário não encontrado com este Id")
        
    def get_by_email(self, user_email: str) -> User:
        try:
            user_model = UserModel.objects.get(email=user_email)
            return user_model.to_domain()
        except UserModel.DoesNotExist:
            raise ValueError("Usuário não encontrado com este e-mail")

    def get_all_paginated_filtered(self, offset: int, limit: int, search_query: str = "") -> tuple[list[User], int]:
        queryset = UserModel.objects.all()

        if search_query:
            queryset = queryset.filter(
                Q(email__icontains=search_query) |
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query)
        )

        total_items = queryset.count()
        paginated = queryset[offset:offset + limit]
        users = [user.to_domain() for user in paginated]

        return users, total_items