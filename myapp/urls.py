from django.urls import path
from . import views

urlpatterns=[
    path("create-user",views.Createuser.as_view(),name ="create-user"),
    # path("password-reset",views.PassWordReceiver.as_view())  
    path("public-question",views.PublicQuestionGV.as_view(),name="publicQuestion")
]