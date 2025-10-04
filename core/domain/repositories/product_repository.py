from core.domain.entities.product import Product
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

class ProductRepository(ABC):
    
    @abstractmethod
    def create(self, product: Product) ->Product:
        """Cria um novo produto"""
        pass
    
    @abstractmethod
    def delete(self, produc_id: str) -> Product:
        """Deleta um Produto.
        -  vai ser implementado na camada de infraestrutura
        """
        pass
    
    @abstractmethod
    def update(self, produc_id: str) -> None:
        """Atualiza um Produto ja existente.
        -  vai ser implementado na camada de infraestrutura
        """
        pass
    
    @abstractmethod
    def get_all(self) -> List[Product]:
        """Lista todos os produtos"""
        pass
    
    @abstractmethod
    def get_by_id(self, product_id: str) -> Optional[Product]:
        """Busca produtos por id"""
        pass
    
    @abstractmethod
    def get_all_paginated_filtered(
        self, offset: int, limit: int, search_query: str | None = None) ->Tuple[List[Product], int]:
        """Lista produtos com paginação e filtro opcional"""
        pass