from django.urls import path
from .views import ProductCreateAPIView, ProductRetrieveAPIView, ProductListAPIView

urlpatterns = [
    path("products/", ProductCreateAPIView.as_view(), name="product-list-create"),
    path("products/list/", ProductListAPIView.as_view(), name="product-list"),
    path("products/<uuid:pk>/", ProductRetrieveAPIView.as_view(), name="product-retrieve"),
]
