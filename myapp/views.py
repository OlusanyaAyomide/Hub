from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import UserSerializer,PublicQuestionSerializer
from .models import UserData,PublicQuestion
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated
from .permissons import PublicQuestionPermission

# Create your views here.

class Createuser(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = UserData.objects.all()


class PublicQuestionGV(generics.ListCreateAPIView):
    permission_classes = [PublicQuestionPermission]
    serializer_class = PublicQuestionSerializer
    
    def get_queryset(self):
        return PublicQuestion.objects.all()

