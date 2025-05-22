from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet
from .models import Product
from .serializers import ProductCollectionSerializer,ProductDetailSerializer
from rest_framework.response import Response

class ProductView(ReadOnlyModelViewSet):
    def get_queryset(self):
        queryset=Product.objects.prefetch_related("product_images").all()
        request=self.request
        params=request.query_params
        print("paramssssssss",params,"is sort")
        sort=params.get("sort")
        cateogry=params.get("cateogry")
        type=params.get("type")
        search=params.get("search")

        if sort:
            if sort=="asc":
                queryset=queryset.order_by("price")
            else:    
                queryset=queryset.order_by("-price")
        if cateogry:
            if cateogry=="Men":
                queryset=queryset.filter(cateogry__parent__name="Men")
            if cateogry=="Women":
                queryset=queryset.filter(cateogry__parent__name="Women")
            if cateogry=="kids"or cateogry=="Kids":
                queryset=queryset.filter(cateogry__parent__name="Kids")
        if type:
            if type=="BottomWear":
                queryset=queryset.filter(cateogry__name='BottomWear')
            if type=="TopWear":
                queryset=queryset.filter(cateogry__name='TopWear')
            if type=="WinterWear":
                queryset=queryset.filter(cateogry__name='WinterWear')
        if search:
            queryset=queryset.filter(name__icontains=search)

        return queryset
        
    
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
        latest_products = Product.objects.order_by('-created_at')[:8]
        best_sellers = Product.objects.filter(bestSeller=True)[:4]

        latest_products_data=ProductCollectionSerializer(latest_products,many=True).data
        best_sellers_data=ProductCollectionSerializer(best_sellers,many=True).data

        return Response({
            "latest_products": latest_products_data,
            "best_sellers": best_sellers_data
        })

