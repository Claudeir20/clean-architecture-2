from abc import ABC, abstractmethod
from typing import Tuple

class AuthGateway (ABC):
    @abstractmethod
    def check_password(self, user_id: str, password: str) -> bool:
        """Verifica se a senha está correta"""
        pass
    
    @abstractmethod
    def set_password(self, user_id: str, new_password: str) -> None:
        """Define nova senha para usuarios"""
        pass
    
    @abstractmethod
    def create_tokens(self, user_id: str) -> Tuple[str, str]:
        """Cria tokens de acesso e refresh"""
        pass