from dataclasses import dataclass, field
import uuid
from core.domain.entities.product import Product
from core.domain.entities.user import User

@dataclass
class Order:
    owner: User
    product: Product
    quantity: int
    subtotal: float
    status: str
    order_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    @property
    def get_subtotal(self) -> float:
       return self.product.price * self.quantity