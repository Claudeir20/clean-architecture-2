from core.domain.entities.order import Order
from core.domain.repositories.order_repository import OrderRepository
from core.domain.entities.product import Product
from dataclasses import dataclass
from typing import List

@dataclass
class CreateOrderRequest:
    owner: str 
    product: Product
    quantity: int
    subtotal: float

@dataclass
class CreateOrderResponse:
    order_id: str
    owner: str 
    product: str
    quantity: int
    subtotal: float
    
class CreateOrderUseCase:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository
    
    def execute(self, request: CreateOrderRequest) -> CreateOrderResponse:
        order = Order(
            owner=request.owner,
            product=request.product,
            quantity=request.quantity,
            subtotal=request.subtotal
        )
        create_order = self.order_repository.create(order)
        
        return CreateOrderResponse(
            order_id=create_order.order_id,
            owner=create_order.owner,
            product=create_order.product,
            quantity=create_order.quantity,
            subtotal=create_order.subtotal
        )


@dataclass
class ListOrdersRequest:
    """
    DTO de entrada para listagem de pedidos com paginação e filtro.

    Attributes:
        offset (int): Posição inicial da listagem.
        limit (int): Quantidade máxima de pedidos a retornar.
        search_query (str | None): Termo de busca opcional.
    """
    offset: int = 0
    limit: int = 10
    search_query: str | None = None

@dataclass
class ListOrdersResponse:
    """
    DTO de saída para listagem de pedidos.

    Attributes:
        orders (list[CreateOrderResponse]): Lista de pedidos encontrados.
        total_items (int): Total de pedidos disponíveis.
        offset (int): Posição inicial da listagem.
        limit (int): Quantidade máxima de pedidos retornados.
    """
    orders: List[CreateOrderResponse]
    total_items: int
    offset: int
    limit: int

class ListOrderUseCase:
    """
    Caso de uso responsável por listar pedidos com suporte a paginação e filtro.

    Utiliza os parâmetros fornecidos em ListOrdersRequest para buscar os pedidos
    no repositório e retorna os resultados em ListOrdersResponse.
    """
    def __init__(self, order_repository: OrderRepository):
        """
        Inicializa o caso de uso com a dependência do repositório de pedidos.

        Args:
            order_repository (OrderRepository): Repositório de pedidos.
        """
        self.order_repository = order_repository
    
    def execute(self, request: ListOrdersRequest) -> ListOrdersResponse:
        """
        Executa a listagem de pedidos com base nos parâmetros de entrada.

        Args:
            request (ListOrdersRequest): Parâmetros de paginação e filtro.

        Returns:
            ListOrdersResponse: Lista de pedidos e metadados de paginação.
        """
        orders_domain, total_items = self.order_repository.get_all_paginated_filtered(
            offset=request.offset,
            limit=request.limit,
            search_query=request.search_query
        )

        orders_response = [
            CreateOrderResponse(
                order_id=order.order_id,
                owner=order.owner,
                product=order.product.name,
                quantity=order.quantity,
                subtotal=order.get_subtotal()
            ) for order in orders_domain
        ]

        return ListOrdersResponse(
            orders=orders_response,
            total_items=total_items,
            offset=request.offset,
            limit=request.limit
        )

