from rest_framework import serializers
from products.models import Product,Category,Size,ProductImage,Category


# serializer to add images for storing products.
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductImage
        fields=["image_url",]


class ProductAddSerializer(serializers.ModelSerializer):
    product_images = serializers.ListField(child=serializers.ImageField(), write_only=True)
    cateogry=serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    # Handle M2M field
    size = serializers.SlugRelatedField(queryset=Size.objects.all(), slug_field="name", many=True)
    class Meta:
        model=Product
        fields=["name","description","price","stock","bestSeller","size","cateogry","product_images"]

    def create(self, validated_data): 
        images = validated_data.pop("product_images")
        size_data = validated_data.pop("size", [])  # Extract size list (["S", "M", "L"])
        product = Product.objects.create(**validated_data)  # Create Product
        product.size.set(size_data)  # Assign ManyToMany sizes
        
        # Create image instances
        ProductImage.objects.bulk_create([
            ProductImage(product=product, image_url=image) for image in images
        ])
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
    cateogry= serializers.CharField(source="parent.name", allow_null=True)
    class Meta:
        model=Product
        fields=["id","main_img","name","price","cateogry"]


    def get_main_img(self,obj):
        print(obj)
        main_img=obj.product_images.filter(is_main=True).first()
        return main_img.image_url.url if main_img else None
    
