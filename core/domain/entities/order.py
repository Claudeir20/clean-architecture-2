from dataclasses import dataclass
from core.domain.entities.product import Product

@dataclass
class Order:
    order_id: str
    owner: str
    product: Product
    quantity: int
    subtotal: float

    @property
    def get_subtotal(self) -> float:
       return self.product.price * self.quantity