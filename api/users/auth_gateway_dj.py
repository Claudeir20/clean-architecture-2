
from core.interfaces.usecase.gateways import AuthGateway
from .models import UserModel
from django.conf import Settings
from django.contrib.auth import authenticate, get_user_model
from django.utils import timezone

class DjangoAuthGateway(AuthGateway):
    def check_password(self, user_id: str, password: str) -> bool:
        try:
            user = UserModel.objects.get(id=user_id)
            result = user.check_password(password)
            return result
        except UserModel.DoesNotExist:
            return False
    
    def set_password(self, user_id: str, new_password: str) -> None:
        try:
            user = UserModel.objects.get(id=user_id)
            user.set_password(new_password)
            user.save()
        except:
            raise ValueError("Usuário não encontrado")