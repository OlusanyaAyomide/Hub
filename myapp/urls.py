from django.urls import path
from . import views

urlpatterns=[
    path("create/user",views.Createuser.as_view(),name ="create-user"),
    path("password/reset",views.PassWordResetLink.as_view()),  
    path("public/question",views.PublicQuestionGV.as_view(),name="publicQuestion"),
    path("public/question/<str:slug>",views.PublicQuestionView.as_view(),name = "question-reply"),
    path("upvote/<str:slug>",views.UpvoteQuestionAV.as_view(),name = "upvote"),
    path("downvote/<str:slug>",views.DownVoteQuestionAV.as_view(),name = "downvote"),
    path("institution/add-view",views.InstitutionAddGV.as_view(),name = "institution"),
    path("subject/create-view",views.SubjectCreateGV.as_view(),name = "subject-create"),
    path("topic/view/<str:pk>",views.TopicViewGV.as_view(),name = "topicView"),
    path("question/upload/<str:institution>/<str:subject>/<str:topic>",views.UploadQuestions.as_view(),name = "upload")
]