from django.urls import path
from . import views

urlpatterns=[
    path("create-user",views.Createuser.as_view(),name ="create-user")   
]