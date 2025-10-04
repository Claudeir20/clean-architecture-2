from core.domain.entities.product import Product
from core.domain.repositories.product_repository import ProductRepository
from .models import ProductModel
from django.db.models import Q

class DjangoProductRepository(ProductRepository):
    def create(self, product: Product) -> Product:
        product = ProductModel.objects.create(
            name= product.name,
            price = product.price,
            stock = product.stock,
            is_active = product.is_active
        )
        return product.to_domain()

    def delete(self, produc_id: Product) -> None:
        delete_product = ProductModel.objects.filter(id= produc_id).delete()
        if delete_product == 0:
            raise ValueError("Produto não encontrado")


    def update(self, product: Product) -> Product:
        model = ProductModel.objects.get(id=product.id)

        model.name = product.name
        model.price = product.price
        model.stock = product.stock
        model.is_active = product.is_active

        model.save()
        return model.to_domain()


    def get_all(self) -> list[Product]:
        return [product_model.to_domain() for product_model in ProductModel.objects.all()]

    def get_by_id(self, product_id: str)-> Product:
        try:
            product_model = ProductModel.objects.get(id=product_id)
            return product_model.to_domain()
        except:
            raise ValueError("Produto não encontrado")
    
    def get_all_paginated_filtered(self, offset: int, limit: int, search_query: str = "") -> tuple[list[Product], int]:
        queryset = ProductModel.objects.all()

        if search_query:
            queryset = queryset.filter(
                Q( name__icontains=search_query)
            )

        total_items = queryset.count()
        paginated = queryset[offset:offset + limit]
        products = [product_model.to_domain() for product_model in paginated]

        return products, total_items