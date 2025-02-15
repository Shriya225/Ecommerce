from rest_framework import serializers
from products.models import Product,Category,Size

class ProductAddSerializer(serializers.ModelSerializer):
    cateogry=serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    # Handle M2M field
    size = serializers.SlugRelatedField(queryset=Size.objects.all(), slug_field="name", many=True)
    class Meta:
        model=Product
        fields=["name","description","price","stock","bestSeller","size","cateogry"]

    def create(self, validated_data):
        size_data = validated_data.pop("size", [])  # Extract size list (["S", "M", "L"])
        product = Product.objects.create(**validated_data)  # Create Product
        product.size.set(size_data)  # Assign ManyToMany sizes
        return product

