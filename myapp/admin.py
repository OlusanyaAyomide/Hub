from django.contrib import admin
from .models import UserData,Question,Instituition,Subject,Topic,PublicQuestion,QuestionReply,InstitutionChat,InstitutionMessage,Userverify
# Register your models here.
admin.site.register([UserData,Question,Instituition,Subject,Topic,PublicQuestion,QuestionReply,InstitutionChat,InstitutionMessage,Userverify])
