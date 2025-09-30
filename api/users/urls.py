from django.urls import path
from .views import UserListCreateAPIView, RetrieveUpdateDestroyAPIView
from .auth import LoginAPIView
urlpatterns = [
    path("users/", UserListCreateAPIView.as_view(), name="user-list-create"),
    path("users/<uuid:pk>/", RetrieveUpdateDestroyAPIView.as_view(), name="user-retrieve"),
    path("login/", LoginAPIView.as_view(), name="login"),
]
