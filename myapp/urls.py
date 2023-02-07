from django.urls import path
from . import views

urlpatterns=[
    path("create-user",views.Createuser.as_view(),name ="create-user"),
    path("password-reset",views.PassWordResetLink.as_view()),  
    path("public-question",views.PublicQuestionGV.as_view(),name="publicQuestion"),
    # path("question-reply/<str:pk>",views.PublicQuestionReplyGV.as_view(),name = "question-reply")
]