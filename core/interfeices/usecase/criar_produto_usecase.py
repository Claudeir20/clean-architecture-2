from core.domain.entities.product import Product
from core.domain.entities.user import User
from core.domain.repositories.product_repository import ProductRepository
from dataclasses import dataclass
from builtins import PermissionError


@dataclass
class CreateProductRequest:
    """
    DTO de entrada para criação de um novo produto.

    Attributes:
        name (str): Nome do produto.
        price (float): Preço do produto.
        stock (int): Quantidade disponível em estoque.
        is_active (bool): Indica se o produto está ativo no catálogo.
    """
    name: str
    price: float
    stock: int
    is_active: bool = True

@dataclass
class CreateProductResponse:
    """
    DTO de saída após a criação de um produto.

    Attributes:
        id (str): Identificador único do produto.
        name (str): Nome do produto.
        price (float): Preço do produto.
        stock (int): Quantidade disponível em estoque.
        is_active (bool): Indica se o produto está ativo no catálogo.
    """
    id: str
    name: str
    price: float
    stock: int
    is_active: bool 

class CreateProductUseCase:
    """
    Caso de uso responsável por criar um novo produto.

    Recebe os dados via CreateProductRequest, instancia a entidade Product
    e delega ao repositório para persistência. Retorna os dados do produto
    criado encapsulados em CreateProductResponse.
    """
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
        """
        Inicializa o caso de uso com a dependência do repositório de produtos.

        Args:
            product_repository (ProductRepository): Repositório de produtos.
        """
    def execute(self, request: CreateProductRequest, current_user: User) -> CreateProductResponse:
        """
        Executa a criação de um novo produto.

        Args:
            request (CreateProductRequest): Dados do produto a ser criado.
            current_user (User): Usuário que está tentando realizar a operação.
            A regra de negócio definida na entidade User será aplicada para verificar
            se o usuário tem permissão para gerenciar produtos (somente administradores).

        Returns:
            CreateProductResponse: Dados do produto criado.

        Raises:
            PermissionError: Se o usuário não tiver permissão para criar produtos
        """
        if not current_user.can_manager_products():
            raise PermissionError("Apenas administradores podem criar produtos.")
        
        product = Product(
            name=request.name,
            price=request.price,
            stock=request.stock,
            is_active=request.is_active
        )
        created_product = self.product_repository.create(product)
        
        return CreateProductResponse(
            id=created_product.id,
            name=created_product.name,
            price=created_product.price,
            stock=created_product.stock,
            is_active=created_product.is_active
        )

@dataclass
class ListProductsRequest:
    """
    DTO de entrada para listagem de produtos com paginação e filtro.

    Attributes:
        offset (int): Posição inicial da listagem.
        limit (int): Quantidade máxima de produtos a retornar.
        search_query (str | None): Termo de busca opcional.
    """
    offset: int = 0
    limit: int = 10
    search_query: str | None = None


@dataclass
class ListProductsResponse:
    """
    DTO de saída para listagem de produtos.

    Attributes:
        products (list[CreateProductResponse]): Lista de produtos encontrados.
        total_items (int): Total de produtos disponíveis.
        offset (int): Posição inicial da listagem.
        limit (int): Quantidade máxima de produtos retornados.
    """
    product: list[CreateProductUseCase]
    total_items: int
    offset: int
    limit: int

class ListProductsUseCase:
    """
    Caso de uso responsável por listar produtos com suporte a paginação e filtro.

    Utiliza os parâmetros fornecidos em ListProductsRequest para buscar os produtos
no repositório e retorna os resultados em ListProductsResponse.
    """
    def __init__(self, product_repository: ProductRepository):
        """
        Inicializa o caso de uso com a dependência do repositório de produtos.

        Args:
            product_repository (ProductRepository): Repositório de produtos.
        """
        self.product_repository = product_repository
    
    def execute(self, request: ListProductsRequest) -> ListProductsResponse:
        """
        Executa a listagem de produtos com base nos parâmetros de entrada.

        Args:
            request (ListProductsRequest): Parâmetros de paginação e filtro.

        Returns:
            ListProductsResponse: Lista de produtos e metadados de paginação.
        """
        product_domain, total_items = self.product_repository.get_all_paginated_filtered(
            offset=request.offset,
            limit=request.limit,
            search_query=request.search_query
        )
        product_response = [
            CreateProductResponse(
                id=product.id,
                name=product.name,
                price=product.price,
                stock=product.stock,
                is_active=product.is_active
            ) for product in product_domain
        ]
        
        return ListProductsResponse(
            products=product_response,
            total_items=total_items,
            offset=request.offset,
            limit=request.limit
        )

@dataclass
class GetProductByIdRequest:
    """
    DTO de entrada para busca de produto por ID.

    Attributes:
        product_id (str): Identificador único do produto.
    """
    product_id: str

class GetProductByIdUseCase:
    """
    Caso de uso responsável por buscar um produto pelo seu ID.

    Recebe um GetProductByIdRequest e retorna os dados do produto
    encapsulados em CreateProductResponse.
    """
    def __init__(self, repo: ProductRepository):
        """
        Inicializa o caso de uso com a dependência do repositório de produtos.

        Args:
            repo (ProductRepository): Repositório de produtos.
        """
        self.repo = repo
    
    def execute(self, request: GetProductByIdRequest)-> CreateProductResponse:
        """
        Executa a busca de um produto pelo ID.

        Args:
            request (GetProductByIdRequest): Contém o ID do produto a ser buscado.

        Returns:
            CreateProductResponse: Dados do produto encontrado.

        Raises:
            ValueError: Se o produto não for encontrado.
        """
        product = self.repo.get_by_id(request.product_id)

        if not product:
            raise ValueError("Produto não encontrado")
        
        return CreateProductResponse(
                id=product.id,
                name=product.name,
                price=product.price,
                stock=product.stock,
                is_active=product.is_active
    )