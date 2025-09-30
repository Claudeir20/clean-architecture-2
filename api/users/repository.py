from core.domain.entities.user import User
from core.domain.repositories.user_repository import UserRepository
from api.users.models import UserModel
from django.db.models import Q

class DjangoUserRepository(UserRepository):
    """
    Implementação concreta do repositório de usuários utilizando o ORM do Django.
    Esta classe conecta a entidade de domínio `User` com o modelo `UserModel` do Django,
    permitindo persistência, recuperação e manipulação de dados de usuários.
    """
    def create(self, user: User) -> User:
        """create(user: User) -> User
        Cria um novo usuário no banco de dados. Verifica se o e-mail já está em uso.
        A senha é criptografada com `set_password()` antes de salvar."""
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
        model.set_password(user.password) 
        model.save()
        return model.to_domain()

    def delete(self, user_id: str) -> None:
        """delete(user_id: str) -> None
        Remove um usuário com base no ID. Lança erro se o usuário não for encontrado.
        """
        delete_count, _ = UserModel.objects.filter(id= user_id).delete()
        if delete_count == 0:
            raise ValueError("Usúario não encontrado")
    
    def update(self, user:User ) ->User:
        """ update(user: User) -> User
        Atualiza os dados de um usuário existente (exceto a senha). Retorna a entidade atualizada.
        """
        model = UserModel.objects.get(id=user.id)
        model.email = user.email
        model.first_name = user.first_name
        model.last_name = user.last_name
        model.save()
        return model.to_domain()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
    
    def get_all(self) -> list[User]:
        """
        get_all() -> list[User]
        Retorna todos os usuários cadastrados como uma lista de entidades de domínio.
        """
        return [user_model.to_domain() for user_model in UserModel.objects.all()]

    
    def get_by_id(self, user_id: str) -> User:
        """get_by_id(user_id: str) -> User
        Busca um usuário pelo ID. Lança erro se não for encontrado.
        """
        try:
            user_model = UserModel.objects.get(id=user_id)
            return user_model.to_domain()
        except:
            raise ValueError("Usuário não encontrado com este Id")
        
    def get_by_email(self, user_email: str) -> User:
        """get_by_email(user_email: str) -> User
        Busca um usuário pelo e-mail. Lança erro se não for encontrado.
        """
        try:
            user_model = UserModel.objects.get(email=user_email)
            return user_model.to_domain()
        except UserModel.DoesNotExist:
            raise ValueError("Usuário não encontrado com este e-mail")

    def get_all_paginated_filtered(self, offset: int, limit: int, search_query: str = "") -> tuple[list[User], int]:
        """get_all_paginated_filtered(offset: int, limit: int, search_query: str = "") -> tuple[list[User], int]
        Retorna uma lista paginada e filtrada de usuários com base em nome ou e-mail.
        Também retorna o total de itens encontrados.
        """
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