from rest_framework import serializers
from .models import Cart,CartItem
from products.models import Product,Size

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cart
        fields="__all__"

class CartProductSerializer(serializers.ModelSerializer):
    main_img=serializers.SerializerMethodField()
    class Meta:
        model=Product
        fields=["name","price","main_img"]
    
    def get_main_img(self,obj):
        print(obj)
        main_img=obj.product_images.filter(is_main=True).first()
        return main_img.image_url.url if main_img else None
    

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Size
        fields=["name",]
    
class CartItemSerializer(serializers.ModelSerializer):
    product=CartProductSerializer()
    size=SizeSerializer()

    class Meta:
        model=CartItem
        fields=["cart_id","quantity","product","size","created_at"]








