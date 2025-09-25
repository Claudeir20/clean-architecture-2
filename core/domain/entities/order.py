from dataclasses import dataclass, field
import uuid
from core.domain.entities.product import Product

@dataclass
class Order:
    owner: str
    product: Product
    quantity: int
    subtotal: float
    order_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    @property
    def get_subtotal(self) -> float:
       return self.product.price * self.quantity