from django.conf import settings
from django.db import models

from store.models import Product


class Order(models.Model):
    class Status(models.TextChoices):
        ORDERED = "ORDERED", "Ordered"  # [ENUM, Label]
        SHIPPED = "SHIPPED", "Shipped"
        DELIVERED = "DELIVERED", "Delivered"
        CANCELLED = "CANCELLED", "Cancelled" 
    
    # since we are using CustomUser Model(not Django's default User Model), 
    # we will use our custom AUTH_USER_MODEL(defined in settings/base.py)
    # on_delete=models.CASCADE: if a user is deleted from db, all its orders would be deleted
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_index=True)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ORDERED, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderItem(models.Model):
    # related_name="items" allows reverse access from Order to OrderItem.
    # so, instead of using the default reverse lookup like order.orderitem_set.all(),
    # we can use order.items.all()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items", db_index=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
