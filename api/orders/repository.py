from core.domain.entities.order import Order
from core.domain.repositories.order_repository import OrderRepository
from .models import OrderModel

class DjangoOrderRepository(OrderRepository):
    def create(self, order: Order) -> Order:
        order_model = OrderModel.objects.create(
            order_id = order.order_id,
            owner = order.owner,
            product = order.product,
            quantity = order.quantity,
            subtotal = order.subtotal,
            status = order.status,
        )
        return order_model.to_domain()

    def get_by_order_id(self, order_id: str)-> Order:
        try:
            order_model = OrderModel.objects.get(id=order_id)
            return order_model.to_domain()
        except:
            raise ValueError("Pedido não encontrado")
        
    def get_all(self)-> list[Order]:
        return [order_model.to_domain() for order_model in OrderModel.objects.all()]
    
    def get_by_owner_id(self, owner_id: str)-> Order:
        try:
            order_model = OrderModel.objects.get(id=owner_id)
            return order_model.to_domain()
        except:
            raise ValueError("Usuário não possui pedidos feito")