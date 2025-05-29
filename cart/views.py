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
        cart_items=CartItem.objects.filter(cart_id=request.user.cart_id)
        serializer=CartItemSerializer(cart_items,many=True)
        return Response({
                         "data":serializer.data,
                        })


class AddCart(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]

    def post(self,request):
        serializer=AddToCartSerializer(data=request.data,context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response({"msg":serializer.data})
        return Response({"msg":serializer.errors})
    
class UpdateCartView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]

    def patch(self,request):
        data=request.data
        cart_item_obj=CartItem.objects.get(id=request.data["id"])
        serializer=AddToCartSerializer(cart_item_obj,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class DeleteCartItemView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    def delete(self, request):
        try:
            data = request.data
            cart_item_id = data.get("id")  # Use `.get()` to avoid KeyError
            
            if not cart_item_id:
                return Response({"error": "ID is required"}, status=400)

            obj = CartItem.objects.get(id=cart_item_id)  # Fetch item
            
            obj.delete()
            return Response({"msg": "Successfully deleted"}, status=200)

        except CartItem.DoesNotExist:
            return Response({"error": "Cart item not found"}, status=404)

        except KeyError:
            return Response({"error": "Invalid request format"}, status=400)

        except Exception as e:  # Handle unexpected errors
            return Response({"error": f"An error occurred: {str(e)}"}, status=500)


