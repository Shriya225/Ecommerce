from django.db import models
from products.models import UUIDModel,Product,Size
from django.contrib.auth.models import User
from uuid import UUID
# Create your models here.


class Cart(UUIDModel):
    user=models.OneToOneField(User, on_delete=models.CASCADE,related_name="cart_id")

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(UUIDModel):
    cart_id=models.ForeignKey(Cart, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size=models.ForeignKey(Size, on_delete=models.CASCADE)
   

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart_id.user.username}'s cart"
