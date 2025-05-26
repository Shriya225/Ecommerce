from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import RegisterSerializer,ProfileSerializer,AdminTokenObtainPairSerializer
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
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
    refresh_token = request.COOKIES.get('refresh_token')
    if not refresh_token:
        return Response({"msg": "No refresh token cookie found"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
    except Exception as e:
        return Response({"msg": f"Error blacklisting token: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
    
    response = Response({"msg": "Successfully logged out."}, status=status.HTTP_200_OK)
    response.delete_cookie('refresh_token', path='/api/login/')
    return response

class ProfileView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]

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
            

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            refresh_token = response.data.get('refresh')
            # Set refresh token in httponly cookie
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                # secure=True,               # Use True in production (HTTPS)
                samesite='Strict',         # or 'Lax' depending on your needs
                max_age=7*24*60*60,        # e.g., 7 days (adjust as needed)
                path='/',
            )
            # Optionally remove refresh token from response body if you want it only in cookie
            del response.data['refresh']

        return response


class CustomTokenRefreshView(APIView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')

        if refresh_token is None:
            return Response({'detail': 'No refresh token in cookie'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)

            response = Response({'access': access_token}, status=200)

            # OPTIONAL: rotate refresh token & set new cookie
            new_refresh = str(refresh)
            response.set_cookie(
                key='refresh_token',
                value=new_refresh,
                httponly=True,
                # secure=True,  # enable in production
                samesite='Strict',
                max_age=7 * 24 * 60 * 60,
                path='/api/refresh/',
            )
            return response

        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)



class AdminTokenObtainPairView(TokenObtainPairView):
    serializer_class = AdminTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            refresh_token = response.data.get('refresh')
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                samesite='Strict',
                max_age=7 * 24 * 60 * 60,  # 7 days
                path='/',
            )
            del response.data['refresh']

        return response
