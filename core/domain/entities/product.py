from dataclasses import dataclass, field
import uuid

@dataclass
class Product:
    name: str = field(compare=False)
    price: float = field(compare=False)
    stock: int = field(compare=False)
    is_active: bool = field(default=True, compare=False)
    id: str = field(default_factory=lambda: str(uuid.uuid4()), compare=True)
    
    def is_available(self) -> bool:
        return self.is_active and self.stock >0


    def reduce_stock(self, quantity: int):
        if quantity > self.stock:
            raise ValueError("Estoque insuficicente")
        self.stock -= quantity