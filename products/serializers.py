from rest_framework import serializers
from .models import (Product,Category,Size,ProductImage)

class ProductCollectionSerializer(serializers.ModelSerializer):
    main_image=serializers.SerializerMethodField()
    class Meta:
        model=Product
        fields=["id","name","price","main_image","cateogry","created_at"]
        depth=2

    # obj represents product instance.

    def get_main_image(self,obj):
        main_img=obj.product_images.filter(is_main=True).first()
        return main_img.image_url.url if main_img else None


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductImage
        fields=["id","image_url","is_main"]


class ProductDetailSerializer(serializers.ModelSerializer):
    product_images=ProductImageSerializer(many=True)
    class Meta:
        model=Product
        fields="__all__"
        depth=2
