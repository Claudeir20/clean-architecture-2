import os
from datetime import timedelta
from typing import Tuple

from core.interfaces.usecase.gateways import AuthGateway
from .models import UserModel
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.utils import timezone
from oauth2_provider.models import AccessToken, Application, RefreshToken
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
        
    def create_tokens(self, user_id: str) -> Tuple[str, str]:

        try:
            user = UserModel.objects.get(id=user_id)
        except UserModel.DoesNotExist:
            raise ValueError("Usuário não encontrado")
            
        try:
            application = Application.objects.get(name= "Default Application")
        except Application.DoesNotExist:
            application = Application.objects.create(
                name="Default Application",
                client_type ="public",
                authorization_grant_type="password",
            )
                
            #Remove quaisquer tokens para usuário e aplicação
        AccessToken.objects.filter(user=user, application=application).delete()
        RefreshToken.objects.filter(user=user, application=application).delete()
            
        access_token = AccessToken.objects.create(
            user=user,
            application=application,
            token="access_token_"
            + str(user_id)
            + "_"
            + os.urandom(30).hex(),  # Gerar um token real
            scope="read write",
            expires=timezone.now()
            + timedelta(
            seconds=settings.OAUTH2_PROVIDER["ACCESS_TOKEN_EXPIRE_SECONDS"]
        ),
    )

        # Crie um novo refresh token
        refresh_token = RefreshToken.objects.create(
            user=user,
            application=application,
            token="refresh_token_"
            + str(user_id)
            + "_"
            + os.urandom(30).hex(),  # Gerar um token real
            access_token=access_token,
        )
            
        return access_token.token, refresh_token.token
