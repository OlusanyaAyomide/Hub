from rest_framework import serializers
from .models import UserData

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ['email','password',"username"]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, value):
        email =  value["email"]
        if UserData.objects.filter(email = email).exists():
            raise serializers.ValidationError("Email Already Exists")
        try:
            value["username"]
        except:
            raise serializers.ValidationError("username field is missing")
        
        return value

    def create(self,validated_data):
        user = UserData.objects.create(
            email = validated_data["email"],
            username = validated_data["username"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user