import uuid
from dataclasses import dataclass, field
class PermissionError(Exception):
    pass

@dataclass
class User:
    email: str = field(compare=True)
    first_name: str = field (compare=False)
    last_name: str = field (compare=False)
    password: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()), compare=True)
    is_active: bool = field(default=True, compare=False)
    is_staff: bool = field(default=False, compare=False)
    is_superuser: bool = field(default=False, compare=False)
    
    
    def is_admin(self) ->bool:
        """verifica se o usuário é administrador
        """
        return self.is_staff and self.is_superuser
    
    def can_manager_products(self) -> bool:
        """Regra de negócio: apenas admins podem gerenciar produtos"""
        if not self.is_admin():
            raise PermissionError("Apenas administradores podem gerenciar produtos")
        return True
    
    def can_view_orders(self, order_owner_id) -> bool:
        """Regra de negóco: Usuario pode ver o pedido ser for o dono"""
        return self.id == order_owner_id or self.is_admin()
    
    def __eq__(self, other):
        """Compara usuàrio por id"""
        if not isinstance(other, User):
            return NotImplemented
        return self.id == other.id
    
    
    def __hash__(self):
        """Hash baseado no id do usuário"""
        return hash(self.id)
    
    
    def __str__(self):
        """Representação string do usuário"""
        return f"User(id={self.id}), email=({self.email})"