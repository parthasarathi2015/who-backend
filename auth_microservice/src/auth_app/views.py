from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView
from rest_framework.permissions import AllowAny
from .serializers import (
    MyTokenObtainPairSerializer,
    CustomTokenObtainPairSerializer,
    CustomTokenVeryfySerializer
)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer


class CustomTokenVerifyView(TokenVerifyView):
    serializer_class = CustomTokenVeryfySerializer


    