from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView
from .views import MyTokenPairView


urlpatterns =[
    path("api/token",MyTokenPairView.as_view()),
    path("api/refresh",TokenRefreshView.as_view()),
    path("api/verify",TokenVerifyView.as_view())
]