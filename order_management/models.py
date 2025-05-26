from django.db import models
from products.models import UUIDModel,Product,Size
from django.contrib.auth.models import User
# Create your models here.

class Order(UUIDModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    PAYMENT_METHODS = [
        ('cod', 'Cash on Delivery'),
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('upi', 'UPI'),
        ('paypal', 'PayPal'),
        ('net_banking', 'Net Banking'),
    ]
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Order {self.id} by {self.user.username} - {self.status}"
    

class OrderItem(UUIDModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.ForeignKey(Size, on_delete=models.CASCADE,null=True,blank=True)  

    # dynamic calculation evry time user changes quantity.
    def total_price(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    

class DeliveryInfo(UUIDModel):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="delivery_info")
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email_address=models.EmailField()
    phone_number = models.CharField(max_length=20)
    street = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

   

