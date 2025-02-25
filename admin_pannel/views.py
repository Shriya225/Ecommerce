from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProductAddSerializer,ListProductSerializer
from products.models import Product
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import transaction
import uuid
from order_management.models import Order,OrderItem
from .serializers import ListOrderSerializer

# Create your views here.

class AddProductView(APIView):
    def post(self,request):
        data=request.data
        print(data)
        serializer=ProductAddSerializer(data=data)
        if serializer.is_valid():
            print("vlaidated")
            serializer.save()
        else:
            print(serializer.errors)
        return Response({"errors":serializer.errors,"data":serializer.data})

class ListProductView(APIView):
    def get(self,request):
        products=Product.objects.all()
        serializer=ListProductSerializer(products)
        return Response(serializer.data)
    

class DeleteProductView(APIView):
    def delete(self, request):
        product_id = request.data.get("id") 

        if not product_id:
            return Response({"msg": "Send a valid product ID"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Ensure product_id is a valid UUID
            product_uuid = uuid.UUID(product_id)
        except ValueError:
            return Response({"msg": "Invalid UUID format"}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, id=product_uuid) 

        try:
            with transaction.atomic():  # Ensures safe rollback if an error occurs
                product.delete()
            return Response({"msg": "Product deleted successfully"}, status=status.HTTP_200_OK)

        except Exception as e: 
            return Response(
                {"msg": "Something went wrong while deleting the product", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    



class ListOrderView(APIView):
    def get(self,request):
        orders=Order.objects.all()
        serializer=ListOrderSerializer(orders,many=True)    
        return Response(serializer.data)
    

class UpdateOrderStatusView(APIView):
    def patch(self, request):
            id = request.data.get("id")
            status_value = request.data.get("status")

            if not id or not status_value:
                return Response({"msg": "ID and status are required"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                obj = Order.objects.filter(id=id).first()
                if obj is None:
                    return Response({"msg": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

                obj.status = status_value
                obj.save()  # Save the updated status

                return Response({"msg": "Order status updated successfully"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"msg": f"Error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
