from core.domain.entities.order import Order
from abc import ABC, abstractmethod
from typing import List, Optional

class OrderRepository(ABC):
    
    @abstractmethod
    def create(self, order : Order) -> Order:
        """Cria um novo pedido"""
        pass

    @abstractmethod
    def get_all(self) -> List[Order]:
        """Lista todos os pedidos"""
        pass

    @abstractmethod
    def get_by_owner_id(self, owner_id: str) -> Optional[Order]:
        """Lista os pedidos por id dos usuários"""
        pass

    @abstractmethod
    def get_by_order_id(self, order_id: str) -> Optional[Order]:
        """Lista os pedidos por id"""
        pass