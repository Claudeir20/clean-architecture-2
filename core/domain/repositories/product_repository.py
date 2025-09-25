from core.domain.entities.product import Product
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

class ProductRepository(ABC):
    
    @abstractmethod
    def create(self, product: Product) ->Product:
        """Cria um novo produto"""
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