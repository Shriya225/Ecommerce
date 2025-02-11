from rest_framework import serializers
from .models import Order,OrderItem
from products.models import Product,ProductImage

class ProductOrderSerializer(serializers.ModelSerializer):
        main_img=serializers.SerializerMethodField()
        class Meta:
            model=Product
            fields=["name","main_img"]
        
        def get_main_img(self,obj):
            print(obj)
            main_img=obj.product_images.filter(is_main=True).first()
            return main_img.image_url.url if main_img else None



    # reverse Fk Serializer usage
class OrderItemSerializer(serializers.ModelSerializer):
        payment_method = serializers.CharField(source="order.payment_method")  # Get from related order
        product=ProductOrderSerializer()
        total_price=serializers.SerializerMethodField()
        class Meta:
            model=OrderItem
            fields=["id","created_at","product","quantity","unit_price","total_price","payment_method"]
        
        def get_total_price(self,obj):
            return obj.total_price()


# class OrderSerializer(serializers.ModelSerializer):
#         items = OrderItemSerializer(many=True, read_only=True)

#         class Meta:
#             model = Order
#             fields = ['id', 'user', 'created_at', 'total_price', 'payment_method','status','items']
