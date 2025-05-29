from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from cart.models import CartItem
from .models import Order,OrderItem,DeliveryInfo
from rest_framework import status
from .serializers import OrderItemSerializer
from django.db import transaction

# Create your views here.

class AddOrderView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        user = request.user
        payment_method = request.data.get("payment_method")
        delivery_data = request.data.get("delivery_data", {})  # Expecting a dict

        if not payment_method:
            return Response({"error": "Please enter payment_method"}, status=status.HTTP_400_BAD_REQUEST)
        if not delivery_data:
            return Response({"error": "Please enter deivery info"}, status=status.HTTP_400_BAD_REQUEST)

        cart_id = user.cart_id
        cart_items = CartItem.objects.filter(cart_id=cart_id)
        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        total_price = sum(item.product.price * item.quantity for item in cart_items)

        try:
            with transaction.atomic():  # Ensures rollback if any error occurs
                # Step 1: Create Order
                order = Order.objects.create(user=user, total_price=total_price, payment_method=payment_method)

                # Step 2: Create Order Items
                order_items = [
                    OrderItem(order=order, product=item.product, quantity=item.quantity, unit_price=item.product.price, size=item.size)
                    for item in cart_items
                ]
                OrderItem.objects.bulk_create(order_items)  # Save order items efficiently

                # Step 3: Create Delivery Info
                delivery_info = DeliveryInfo.objects.create(
                    order=order,
                    first_name=delivery_data.get("first_name"),
                    last_name=delivery_data.get("last_name"),
                    email_address=delivery_data.get("email_address"),
                    phone_number=delivery_data.get("phone_number"),
                    street=delivery_data.get("street"),
                    city=delivery_data.get("city"),
                    postal_code=delivery_data.get("postal_code"),
                    country=delivery_data.get("country"),
                    state=delivery_data.get("state"),
    
                )

                # Step 4: Clear Cart
                cart_items.delete()

                return Response({"msg": "Successfully created order.", "order_id": str(order.id)}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": "Something went wrong", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ListOrderView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]

    def get(self,request):
        # use double fk lookup form ORM
        orders = OrderItem.objects.filter(order__user=request.user)  
        
        serializer = OrderItemSerializer(orders, many=True)  # Serialize the data
        return Response(serializer.data, status=status.HTTP_200_OK)

