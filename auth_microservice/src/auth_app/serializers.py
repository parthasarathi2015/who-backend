
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenVerifySerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email

        return token

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        print("attr:",attrs)
        data = super().validate(attrs)
        data['user_id'] = self.user.id
        return data


class CustomTokenVeryfySerializer(TokenVerifySerializer):
    def validate(self, attrs):
        #  logic for auth token validity
        return True
