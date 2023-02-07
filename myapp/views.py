from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import UserSerializer,PublicQuestionSerializer,PublicQuestionReplySerializer
from .models import UserData,PublicQuestion,QuestionReply,Userverify
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated
from .permissons import PublicQuestionPermission
import requests
from .helper import randumNumber

# Create your views here.

class Createuser(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = UserData.objects.all()


class PublicQuestionGV(generics.ListCreateAPIView):
    permission_classes = [PublicQuestionPermission]
    serializer_class = PublicQuestionSerializer
    
    def get_queryset(self):
        return PublicQuestion.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(createdBy = user,isActive = True)


# class PublicQuestionReplyGV(generics.ListCreateAPIView):
#     lookup_field = "Pk"
#     serializer_class = PublicQuestionReplySerializer
#     permission_classes = [PublicQuestionPermission]

#     def get_queryset(self):
#         questionId = self.kwargs["pk"]
#         question = PublicQuestion.objects.get(pk = questionId)
#         return QuestionReply.objects.filter(question = question)
    
#     def perform_create(self, serializer):
#         user = self.request.user
#         questionId = self.kwargs["pk"]
#         question = PublicQuestion.objects.get(pk = questionId)
#         serializer.save(question = question,replyBy = user)
    
class PassWordResetLink(APIView):
    def post (self,request):
        email = request.query_params["email"]
        if not UserData.objects.filter(email = email).exists():
            return Response({"response":"User not found"},status=400)
        number = randumNumber()
        user = UserData.objects.get(email = email)
        if Userverify.objects.filter(user = user).exists():
            token = Userverify.objects.get(user = user)
            token.delete()
            print("Deleting")
        r = requests.post('https://bdf4-105-112-38-45.eu.ngrok.io/api/mail/send', data = {
            'receiver_address':email,"content":number,"subject":"Password reset"
        })
        print(r.status_code)
        if r.status_code == 250:
            print("Savinggg")
            Userverify.objects.create(user = user,resetPassword = number )
            return Response({"res":"Confirmation URL sent"})
        return Response({"res":"Something went wrong"},status=400)

        



