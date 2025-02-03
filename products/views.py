from rest_framework.viewsets import ModelViewSet
from .models import Product
from .serializers import ProductSerializer


class ProductView(ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
