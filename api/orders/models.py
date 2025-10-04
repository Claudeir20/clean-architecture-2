from django.db import models
import uuid
from core.domain.entities.order import Order as DomainOrder
from api.users.models import UserModel
from api.products.models import ProductModel
# Create your models here.

class OrderModel(models.Model):
    STATUS_CHOICE =(
        ('p', 'Pendente'),
        ('F', 'Finalizado'),
        ('c', 'Concluído')
    )
    
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner= models.ForeignKey(UserModel, on_delete=models.PROTECT)
    product = models.ManyToManyField(ProductModel, related_name='orders_item')
    quantity = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, default="p")
    
    def to_domain(self) -> DomainOrder:
        return DomainOrder(
            order_id=(self.order_id),
            owner= self.owner,
            product= self.product,
            quantity=self.quantity,
            subtotal=self.subtotal,
            status= self.status
        )