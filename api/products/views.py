from rest_framework import generics, status
from rest_framework.response import Response
from .repository import DjangoProductRepository
from .serializers import ProductSerializer, ProductReadSerializer
from .models import ProductModel
from  core.domain.entities.product import Product
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from core.interfaces.usecase.criar_produto_usecase import(
    CreateProductUseCase,
    ListProductsUseCase,
    GetProductByIdUseCase,
    GetProductByIdRequest,
    ListProductsRequest
)


class ProductListAPIView(generics.ListAPIView):
    queryset = ProductModel.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == "GET":
            return ProductReadSerializer
        return True
    
    def get(self, request):
        repo = DjangoProductRepository()
        use_case = ListProductsUseCase(repo)
        
        request_data = ListProductsRequest(offset=0, limit=10)
        response_data = use_case.execute(request_data)
        
        serializer = self.get_serializer(response_data.products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class ProductCreateAPIView(generics.CreateAPIView):
    queryset = ProductModel.objects.all()
    permission_classes = [IsAdminUser]
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProductSerializer
        return ProductReadSerializer


    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        repo = DjangoProductRepository()
        use_case = CreateProductUseCase(repo)

        request_data = serializer.to_internal_value(request.data)
        domain_user = request.user.to_domain()
        product = use_case.execute(request_data, current_user=domain_user)

        response_serializer = ProductReadSerializer(product)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class RetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """ Retrive:
            Busca um único produto por ID.
        
        Update:
            Atualiza um produto existente.
        
        Destroy:
            Deleta um prooduto.
    """
    queryset = ProductModel.objects.all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return ProductSerializer
        return ProductReadSerializer

    def retrieve(self, request, *args, **kwargs):
        product_id = kwargs['pk']
        repo = DjangoProductRepository()
        use_case = GetProductByIdUseCase(repo)

        try:
            product = use_case.execute(GetProductByIdRequest(product_id=str(product_id)))
            serializer = ProductReadSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        product_id = kwargs['pk']
        repo = DjangoProductRepository()

        # Busca o produto atual.
        get_product_use_case = GetProductByIdUseCase(repo)
        existing_product = get_product_use_case.execute(GetProductByIdRequest(product_id=product_id))

        # Valida os dados recebidos
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Monta o objeto atualizado.
        updated_product = Product(
            id=existing_product.id,
            name=serializer.validated_data.get('name', existing_product.name),
            price=serializer.validated_data.get('price', existing_product.price),
            stock=serializer.validated_data.get('stock', existing_product.stock),
            is_active=serializer.validated_data.get('is_active', existing_product.is_active)
        )

        updated_product = repo.update(updated_product)
        response_serializer = ProductReadSerializer(updated_product)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


    def destroy(self, request, *args, **kwargs):
        product_id = kwargs['pk']
        repo = DjangoProductRepository()

        try:
            repo.delete(product_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
