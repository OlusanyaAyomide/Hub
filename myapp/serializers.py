from rest_framework import serializers
from .models import UserData,PublicQuestion,QuestionReply,Instituition,Question,Topic,Subject,InstitutionMessage
from django.shortcuts import get_object_or_404

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ["id",'email','password',"username","is_verified"]
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


class PublicQuestionReplySerializer(serializers.ModelSerializer):
    replyBy = serializers.StringRelatedField()
    inUpvote = serializers.SerializerMethodField()
    inDownVote = serializers.SerializerMethodField()
    voteCount = serializers.SerializerMethodField()

    class Meta:
        model =QuestionReply
        fields = ["id",'replyBy','replyText','created','inUpvote','inDownVote',"voteCount","slug"]

    def get_inUpvote(self,value):
        user = self.context["request"].user
        if user in value.upvotes.all():
            return True
        return False
   
    
    def get_inDownVote(self,value):
        user = self.context["request"].user
        if user in value.downVotes.all():
            return True
        return False
    
    def get_voteCount(self,value):
        upvote = value.upvotes.all().count()
        downvote = value.downVotes.all().count()
        return upvote - downvote


class PublicQuestionSerializer(serializers.ModelSerializer):
    createdBy =serializers.StringRelatedField()
    questionReply = serializers.SerializerMethodField()
    class Meta:
        model = PublicQuestion
        fields = "__all__"
        extra_kwargs = {
            'questionReply': {'write_only': True}
        }

    def get_questionReply(self,obj):
        question = get_object_or_404(PublicQuestion,pk = obj.id)
        replies = QuestionReply.objects.filter(question = question)
        serializer = PublicQuestionReplySerializer(replies,many = True,context = {
            "request":self.context["request"]
        })
        return serializer.data

class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instituition
        fields = "__all__"

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"

class TopicSerializer(serializers.ModelSerializer):
    subject = serializers.StringRelatedField()
    class Meta:
        model = Topic
        fields = "__all__"

class QuestionSerializer(serializers.ModelSerializer):
    Instituition = InstitutionSerializer(read_only = True,many = True)
    class Meta:
        model = Question
        exclude = ["subject"]
        read_only_fields = ['topic', 'questionId','subject',"Instituition"]


# class InstitutionMessageSerializer(serializers.ModelSerializer):
#     roomName = serializers.StringRelatedField()
#     messageBy = UserData(read_only = True)
#     class Meta:
#         model = InstitutionMessage
#         fields = "__all__"
        
  
        