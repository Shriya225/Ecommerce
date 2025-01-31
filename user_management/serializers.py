from rest_framework import serializers
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=["username","password"]
    def create(self, validated_data):
        print(validated_data,type(validated_data))
        user=User.objects.create(username=validated_data["username"])
        user.set_password(validated_data["password"])
        user.save()
        return user
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["username","email","first_name","last_name"]