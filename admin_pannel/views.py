from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProductAddSerializer

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
