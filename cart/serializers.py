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
        fields=["id","cart_id","quantity","product","size","created_at"]



class AddToCartSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())  # Accepts Product ID
    size = serializers.CharField()  # Accepts size as string

    class Meta:
        model = CartItem
        fields = ["id","quantity", "product", "size"]
    
    
    def validate_size(self, value):
        """Validate size exists in the database."""
        size_obj = Size.objects.filter(name=value).first()
        if not size_obj:
            raise serializers.ValidationError("Invalid size selected.")
        return size_obj  # Return the Size object instead of a string  

    def create(self, validated_data):
        user = self.context["request"].user  # Get user from request
        validated_data["cart_id"] = user.cart_id
        print(user.cart_id)  # Assign cart_id automatically

        # to avoid duplicates of cart items.
        existing_obj=CartItem.objects.filter(cart_id= user.cart_id,product=validated_data["product"],size=validated_data["size"]).first()
        if existing_obj:
            if validated_data.get("quantity"):
                existing_obj.quantity+= validated_data["quantity"]
            else:
                existing_obj.quantity+= 1
            existing_obj.save()
            return existing_obj  # Return updated item
        return CartItem.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        print(instance,type(instance),instance.quantity)
        print(validated_data,type(validated_data))
        updated_quantity=validated_data.get("quantity")
        if not updated_quantity:
            raise serializers.ValidationError("Quantity field is empty..")
        if updated_quantity>=1:
            instance.quantity=validated_data["quantity"]
        else:
            raise serializers.ValidationError("Quantity must be >= 1")
        instance.save()
        return  instance

    










