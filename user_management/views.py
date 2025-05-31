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
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
import os

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
    refresh_token = request.COOKIES.get('refresh_token_user')
    if not refresh_token:
        return Response({"msg": "No refresh token cookie found"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
    except Exception as e:
        return Response({"msg": f"Error blacklisting token: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
    
    response = Response({"msg": "Successfully logged out."}, status=status.HTTP_200_OK)
    response.delete_cookie('refresh_token_user', path='/')
    return response


@api_view(["POST"])
def admin_logout(request):
    refresh_token = request.COOKIES.get('refresh_token_admin')
    if not refresh_token:
        return Response({"msg": "No refresh token cookie found"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
    except Exception as e:
        return Response({"msg": f"Error blacklisting token: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
    
    response = Response({"msg": "Successfully logged out."}, status=status.HTTP_200_OK)
    # Delete cookie with matching path (usually '/')
    response.delete_cookie('refresh_token_admin', path='/')
    return response

class ProfileView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]

    def get(self,request):
        try:
            user=request.user
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
                key='refresh_token_user',
                value=refresh_token,
                httponly=True,
                secure=True,               # Use True in production (HTTPS)
                samesite='None',      
                max_age=7*24*60*60,     
                path='/',
            )
            del response.data['refresh']

        return response


class CustomTokenRefreshView(APIView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token_user')

        if refresh_token is None:
            return Response({'detail': 'No refresh token in cookie'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)

            response = Response({'access': access_token}, status=200)

            # OPTIONAL: rotate refresh token & set new cookie
            new_refresh = str(refresh)
            response.set_cookie(
                key='refresh_token_user',
                value=new_refresh,
                httponly=True,
                secure=True,  # enable in production
                samesite='None',
                max_age=7 * 24 * 60 * 60,
                path='/',
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
                key='refresh_token_admin',
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite='None',
                max_age=7 * 24 * 60 * 60,  # 7 days
                path='/',
            )
            del response.data['refresh']

        return response


class AdminTokenRefreshView(APIView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token_admin') 

        if refresh_token is None:
            return Response({'detail': 'No refresh token in cookie'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)

            response = Response({'access': access_token}, status=200)

            # OPTIONAL: rotate refresh token and reset the cookie
            new_refresh = str(refresh)
            response.set_cookie(
                key='refresh_token_admin',
                value=new_refresh,
                httponly=True,
                secure=True,
                samesite='None',
                max_age=7 * 24 * 60 * 60,
                path='/',  # Scope refresh cookie tightly to admin path
            )

            return response

        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
