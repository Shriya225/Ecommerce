from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=["username","password"]
    def create(self, validated_data):
        user=User.objects.create(username=validated_data["username"])
        user.set_password(validated_data["password"])
        user.save()
        return user
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["username","email","first_name","last_name"]



class AdminTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        if not self.user.is_staff:
            raise serializers.ValidationError("You do not have admin access.")

        data['user'] = {
            'username': self.user.username,
            'is_staff': self.user.is_staff,
            'is_superuser': self.user.is_superuser,
        }
        return data
