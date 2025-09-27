from rest_framework import serializers
from .models import ProductModel
from core.interfaces.usecase.criar_produto_usecase import (
    CreateProductRequest,
    CreateProductResponse
)

class ProductSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField()
    price = serializers.DecimalField( max_digits=10, decimal_places=2)
    stock = serializers.IntegerField()
    is_active = serializers.BooleanField()
    
    def to_internal_value(self, data):
        return CreateProductRequest(
            name=data.get("name"),
            price=data.get("price"),
            stock=data.get("stock"),
            is_active= True
        )

class ProductReadSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    price = serializers.CharField(read_only=True)
    stock = serializers.CharField(read_only=True)
    is_active = True
    def to_representation(self, instance: CreateProductResponse):
        return {
            "id":instance.id,
            "name": instance.name,
            "price": instance.price,
            "stock": instance.stock,
            "is_active": instance.is_active
        }             