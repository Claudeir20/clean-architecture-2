from django.urls import path
from .views import ProductListCreateAPIView, ProductRetrieveAPIView

urlpatterns = [
    path("products/", ProductListCreateAPIView.as_view(), name="product-list-create"),
    path("products/<uuid:pk>/", ProductRetrieveAPIView.as_view(), name="product-retrieve"),
]
