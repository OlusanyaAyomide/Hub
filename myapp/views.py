from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import UserSerializer
from .models import UserData


# Create your views here.

class Createuser(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = UserData.objects.all()