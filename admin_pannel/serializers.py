from rest_framework import serializers
from products.models import Product,Category,Size,ProductImage,Category
from order_management.models import Order,OrderItem,DeliveryInfo

# serializer to add images for storing products.
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductImage
        fields=["image_url",]


class ProductAddSerializer(serializers.ModelSerializer):
    product_images = serializers.ListField(child=serializers.ImageField(), write_only=True)
    category = serializers.CharField(write_only=True)
    subcategory = serializers.CharField(write_only=True)
    size = serializers.SlugRelatedField(queryset=Size.objects.all(), slug_field="name", many=True)
    class Meta:
        model=Product
        fields=["name","description","price","stock","bestSeller","size","category","subcategory","product_images"]
    def validate(self, attrs):
            category_name = attrs.pop("category")
            subcategory_name = attrs.pop("subcategory")

            try:
                parent_category = Category.objects.get(name=category_name, parent=None)
            except Category.DoesNotExist:
                raise serializers.ValidationError({"category": f"Category '{category_name}' not found."})

            try:
                subcategory = Category.objects.get(name=subcategory_name, parent=parent_category)
            except Category.DoesNotExist:
                raise serializers.ValidationError({"subcategory": f"Subcategory '{subcategory_name}' not found under '{category_name}'."})

            attrs["cateogry"] = subcategory  # final FK object
            return attrs
    def create(self, validated_data):
        images = validated_data.pop("product_images")
        size_data = validated_data.pop("size", [])
        category = validated_data.pop("cateogry")  # resolved from validate

        product = Product.objects.create(**validated_data, cateogry=category)
        product.size.set(size_data)
        
        product_images = [
        ProductImage(product=product, image_url=image, is_main=(i == 0))
        for i, image in enumerate(images)]
        ProductImage.objects.bulk_create(product_images)
        return product

# # serilaizer for returning only parent name of cateogry.
# class parentSerializer(serializers.ModelSerializer):
#         class Meta:
#             model=Category
#             fields=["name",]

# serializer for category listproduct
class CateogryProductSerializer(serializers.ModelSerializer):
    parent = serializers.CharField(source="parent.name", allow_null=True)
    class Meta:
        model=Category
        fields=["parent",]


  
# serializer to display all products in admin pannel
class ListProductSerializer(serializers.ModelSerializer):
    main_img=serializers.SerializerMethodField()
    cateogry= serializers.CharField(source="cateogry.parent.name", allow_null=True)
    class Meta:
        model=Product
        fields=["id","main_img","name","price","cateogry"]


    def get_main_img(self,obj):
        print(obj)
        main_img=obj.product_images.filter(is_main=True).first()
        return main_img.image_url.url if main_img else None
    
class DeliveryInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model=DeliveryInfo
        fields=["first_name","city","country","state","postal_code","street"]

# serializer to dispaly all orders
class ListOrderSerializer(serializers.ModelSerializer):
    items=serializers.SerializerMethodField()
    delivery_info=DeliveryInfoSerializer()
    user= serializers.CharField(source="user.username", allow_null=True)
    class Meta:
        model=Order
        fields=["id","created_at","total_price","payment_method","status","delivery_info","items","user"]

    def get_items(self,obj):
        items_data=obj.items.all()
        print(items_data)
        return  [str(item) for item in items_data]  # Calls __str__ method of Product model