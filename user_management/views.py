from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import RegisterSerializer,ProfileSerializer
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
# Create your views here.


class RegisterUserView(APIView):
    def post(self,request):
        try:
            serializer=RegisterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"data":serializer.data,"msg":"succesfully created user."})
            return Response({"errors":serializer.errors,"msg":"cannot create user."},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            raise serializers.ValidationError({"msg":str(e)})

@api_view(["POST"])
def logout(request):
    try:
        refresh_token=request.data.get("refresh")
        if not refresh_token:
            return Response({"msg":"could not get token"})
        token=RefreshToken(refresh_token)
        token.blacklist()
        return Response({"msg":"succesfully logged out."})
    except Exception as e:
        return Response({"msg":str(e)})
    

class ProfileView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]

    #Display Profile details
    def get(self,request):
        print(request.user,type(request.user))
        try:
            user=request.user
            print(user,type(user))
            serializer=ProfileSerializer(user)
            return Response(serializer.data)
        except Exception as e:
            return Response({"msg":str(e)})
    #update Profile
    def patch(self,request):
        serializer=ProfileSerializer(request.user,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg":"succesfully updated User Profile","data":serializer.data})
        return Response({"msg":"error updating.","data":serializer.errors})
    
    # Delete Account
    def delete(self,request):
        try:
            request.user.delete()
            return Response({"msg":"succesfully deleted account"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"msg":"Error deleteing User Profile.","error":str(e)},status=status.HTTP_400_BAD_REQUEST)
            




