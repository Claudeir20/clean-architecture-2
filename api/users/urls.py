from django.urls import path
from .views import UserListCreateAPIView, UserRetriveAPIView

urlpatterns = [
    path("users/", UserListCreateAPIView.as_view(), name="user-list-create"),
    path("users/<uuid:pk>/", UserRetriveAPIView.as_view(), name="user-retrieve"),
]
