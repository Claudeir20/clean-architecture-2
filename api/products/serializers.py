from rest_framework import serializers
from .models import ProductModel
from core.interfaces.usecase.criar_produto_usecase import (
    CreateProductRequest,
    CreateProductResponse
)

class ProductSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    stock = serializers.IntegerField()
    is_active = serializers.BooleanField()

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.stock = validated_data.get('stock', instance.stock)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        return instance



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