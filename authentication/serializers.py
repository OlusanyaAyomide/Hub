from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import time
import math


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['name'] = user.name
        token['email'] = user.email
        token['issued'] = math.floor(time.time())

        return token