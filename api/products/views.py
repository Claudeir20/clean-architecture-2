from rest_framework import generics, status
from rest_framework.response import Response
from .repository import DjangoProductRepository
from .serializers import ProductSerializer, ProductReadSerializer
from .models import ProductModel
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

class ProductRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = ProductReadSerializer
    permission_classes = [IsAdminUser]
    def retrieve(self, request, *args, **kwargs):
        product_id = kwargs['pk']
        get_product_request = GetProductByIdRequest(product_id= str(product_id))
        
        repo = DjangoProductRepository()
        get_product_use_case = GetProductByIdUseCase(repo)

        try:
            product_response = get_product_use_case.execute(get_product_request)
            response_serializer = ProductReadSerializer(instance=product_response)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)