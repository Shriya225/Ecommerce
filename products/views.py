from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet
from .models import Product
from .serializers import ProductCollectionSerializer,ProductDetailSerializer
from rest_framework.response import Response


class ProductView(ReadOnlyModelViewSet):
    queryset=Product.objects.prefetch_related("product_images").all()
    
    def get_serializer_class(self):
        if self.action=="list":
            return ProductCollectionSerializer
        return ProductDetailSerializer

class HomeView(ReadOnlyModelViewSet):
    queryset=Product.objects.prefetch_related("product_images").all()
       
    def get_serializer_class(self):
        if self.action=="list":
            return ProductCollectionSerializer
        return ProductDetailSerializer

    def list(self, request, *args, **kwargs):
        latest_products = Product.objects.order_by('-created_at')[:2]
        best_sellers = Product.objects.filter(bestSeller=True)[:1]

        latest_products_data=ProductCollectionSerializer(latest_products,many=True).data
        best_sellers_data=ProductCollectionSerializer(best_sellers,many=True).data

        return Response({
            "latest_products": latest_products_data,
            "best_sellers": best_sellers_data
        })

