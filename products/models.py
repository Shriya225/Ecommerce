from django.db import models
import uuid
from cloudinary_storage.storage import MediaCloudinaryStorage
class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)  # Set on creation
    updated_at = models.DateTimeField(auto_now=True)  # Set on update

    class Meta:
        abstract = True  # Make this an abstract base class



class Category(UUIDModel):
    name=models.CharField(max_length=30)
    parent=models.ForeignKey("self",blank=True,null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.name if not self.parent else f"{self.parent} --> {self.name}"


class Size(UUIDModel):
    name = models.CharField(max_length=5)

    def __str__(self):
        return self.name

 
class Product(UUIDModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    cateogry=models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    bestSeller=models.BooleanField(default=False)
    size = models.ManyToManyField(Size,related_name="products")  # Many-to-Many since a product can have multiple sizes

    def __str__(self):
        return self.name



class ProductImage(UUIDModel):
    product=models.ForeignKey(Product,on_delete=models.CASCADE, related_name="product_images")
    image_url = models.ImageField(upload_to="product_images/", storage=MediaCloudinaryStorage() )
    is_main=models.BooleanField(default=False)

    def __str__(self):
        return f" Image for {self.product.name}"









