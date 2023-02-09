from rest_framework import serializers
from .models import UserData,PublicQuestion,QuestionReply

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ['email','password',"username","is_verified"]
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

    class Meta:
        model =QuestionReply
        fields = ['replyBy','replyText','created','inUpvote','inDownVote']

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
        print("passed 1")
        question = PublicQuestion.objects.get(pk = obj.id)
        replies = QuestionReply.objects.filter(question = question)
        print(self.context)
        serializer = PublicQuestionReplySerializer(replies,many = True,context = {
            "request":self.context["request"]
        })
        return serializer.data
        # else:
        #     replies = QuestionReply.objects.all()
 
