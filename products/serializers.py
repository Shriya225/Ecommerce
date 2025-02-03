from rest_framework import serializers
from .models import (Product,Category,Size,ProductImage)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields="__all__"
        depth=2
