from django.db import models
import uuid
from core.domain.entities.product import Product as DomainProduct

# Create your models here.

class ProductModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    
    def to_domain(self) ->DomainProduct:
        return DomainProduct(
            id=str(self.id),
            name=self.name,
            price=float(self.price),
            stock=self.stock,
            is_active=self.is_active
        )

    def __str__(self):
        return self.name