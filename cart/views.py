from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CartItem
from products.models import Size
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import CartSerializer,CartItemSerializer,AddToCartSerializer


class ViewCart(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]

    def get(self,request):
        print(request.user,request.user.cart_id)
        cart_items=CartItem.objects.filter(cart_id=request.user.cart_id)
        print(cart_items)
        serializer=CartItemSerializer(cart_items,many=True)
        return Response({
                         "data":serializer.data,
                        })


class AddCart(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]

    def post(self,request):
        print(request.data,type(request.data))  
        serializer=AddToCartSerializer(data=request.data,context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response({"msg":serializer.data})
        return Response({"msg":serializer.errors})


