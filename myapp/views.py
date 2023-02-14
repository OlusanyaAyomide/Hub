from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import UserSerializer,PublicQuestionSerializer,PublicQuestionReplySerializer,InstitutionSerializer,SubjectSerializer,TopicSerializer,QuestionSerializer
from .models import UserData,PublicQuestion,QuestionReply,Userverify,Instituition,Subject,Topic,InstitutionChat
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .permissons import PublicQuestionPermission,AdminOrGetpermission
import requests
from .helper import randumNumber
from django.shortcuts import get_object_or_404

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

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
        

    
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
        r = requests.post('https://bdf4-105-112-38-45.eu.ngrok.io/api/mail/send', data = {
            'receiver_address':email,"content":number,"subject":"Password reset"
        })
        if r.status_code == 250:
            Userverify.objects.create(user = user,resetPassword = number )
            return Response({"res":"Confirmation URL sent"})
        return Response({"res":"Something went wrong"},status=400)

        

#Get request to view all Puiblic Question post requst to add a new public Question

class PublicQuestionView(APIView):
    permission_classes=[PublicQuestionPermission]
    def get(self,request,slug):
        question = get_object_or_404(PublicQuestion,slug = slug)
        serializer = PublicQuestionSerializer(question,context={"request":request,"slug":slug})
        return Response(serializer.data)
    
    def post(self,request,slug):
        question = get_object_or_404(PublicQuestion,slug = slug)
        serializer = PublicQuestionReplySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(question = question,replyBy = request.user)
            newserializer = PublicQuestionSerializer(question,context = {"request":request,"slug":slug})
            return Response(newserializer.data)
        return Response(serializer.errors)


#Upvote public question reply 
class UpvoteQuestionAV(APIView):
    permission_classes =[IsAuthenticated]
    def post(self,request,slug):
        reply = get_object_or_404(QuestionReply,slug = slug)
        if request.user in reply.downVotes.all():
            reply.downVotes.remove(request.user)
        reply.upvotes.add(request.user)
        question = reply.question
        serializer = PublicQuestionSerializer(question,context={"request":request,"slug":slug})
        return Response(serializer.data)


#Downvote public question reply 
class DownVoteQuestionAV(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,slug):
        reply = get_object_or_404(QuestionReply,slug = slug)
        if request.user in reply.upvotes.all():
            reply.upvotes.remove(request.user)
        reply.downVotes.add(request.user)
        question = reply.question
        serializer = PublicQuestionSerializer(question,context={"request":request,"slug":slug})
        return Response(serializer.data)


#View to add a new institution and creating an institution chatroom simultaneously

class InstitutionAddGV(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class =  InstitutionSerializer
    queryset = Instituition.objects.all()

    def perform_create(self, serializer):
        name = self.request.data["name"]
        object  = serializer.save()
        InstitutionChat.objects.create(name = f'{name} Community',institution = object)


class SubjectCreateGV(generics.ListCreateAPIView):
    permission_classes = [AdminOrGetpermission]
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


#Get all Topic for a subject
class TopicViewGV(generics.ListCreateAPIView):
    permission_classes = [AdminOrGetpermission]
    serializer_class = TopicSerializer
    def get_queryset(self):
        pk = self.kwargs["pk"]
        subject = get_object_or_404(Subject,pk = pk)
        return Topic.objects.filter(subject = subject)
    
    def perform_create(self, serializer):
        pk = self.kwargs["pk"]
        subject = get_object_or_404(Subject,pk = pk)
        serializer.save(subject =  subject)

class UploadQuestions(generics.CreateAPIView):
    permission_classes = [AdminOrGetpermission]
    serializer_class = QuestionSerializer
    def perform_create(self, serializer):
        topic = get_object_or_404(Topic,pk = self.kwargs["topic"]) 
        institution =  self.request.data["institution"]
        subject = get_object_or_404(Subject,pk = self.kwargs["subject"])
        object = serializer.save(topic = topic,subject = subject)
        objectArray  = []
        for i in institution:
            item = get_object_or_404(Instituition,pk = i)
            objectArray.append(item)
        object.Instituition.add(*objectArray)
    
