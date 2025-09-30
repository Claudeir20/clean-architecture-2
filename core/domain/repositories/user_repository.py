from abc import ABC, abstractmethod
from core.domain.entities.user import User
from typing import List, Optional, Tuple

class UserRepository(ABC):
    
    
    @abstractmethod
    def create(self, user: User) -> User:
        """Cria novo usuário"""
        pass

    @abstractmethod
    def delete(self, user_id: str) -> None:
        """Deleta um usuário"""
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        """Atualiza um usuário"""
        pass

    
    @abstractmethod
    def get_all(self, user: User) -> List[User]:
        """Lista todos usários"""
        pass
    
    @abstractmethod
    def get_by_id(self, user_id: str) -> Optional[User]:
        """Busca usuários por id"""
        pass
    
    @abstractmethod
    def get_by_email(self, user: User) -> Optional[User]:
        """Busca usuários por email"""
        pass

    @abstractmethod
    def get_all_paginated_filtered(
        self, offset: int, limit: int, search_query: str | None = None) ->Tuple[List[User], int]:
        """Lista usuarios com paginação e filtro opcional"""
        pass