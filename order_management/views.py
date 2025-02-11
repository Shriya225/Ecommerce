from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from cart.models import CartItem
from .models import Order,OrderItem
from rest_framework import status
from .serializers import OrderItemSerializer
from rest_framework import serializers
# Create your views here.

class AddOrderView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]

    def post(self,request):
        user=request.user
        payment_method=request.data.get("payment_method")
        if not payment_method:
            raise serializers.ValidationError("Please Enter Payment_method")
        cart_id=user.cart_id
        cart_items=CartItem.objects.filter(cart_id=cart_id)
        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        order=Order.objects.create(user=user,total_price=total_price,payment_method=request.data.get("payment_method"))
        
        order_items=[
            OrderItem(order=order,product=item.product, quantity=item.quantity, unit_price=item.product.price,size=item.size)
            for item in cart_items
        ]
        OrderItem.objects.bulk_create(order_items)  # Save order items efficiently
        cart_items.delete()  # Clear the cart after ordering

        return Response({"msg":"successfully created order."}, status=status.HTTP_201_CREATED)


class ListOrderView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]

    def get(self,request):
        # use double fk lookup form ORM
        orders = OrderItem.objects.filter(order__user=request.user)  
        print(orders)  # Debugging
        
        serializer = OrderItemSerializer(orders, many=True)  # Serialize the data
        return Response(serializer.data, status=status.HTTP_200_OK)

