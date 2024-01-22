from rest_framework import serializers
from .models import CustomUserModel
from dj_rest_auth.registration.serializers import RegisterSerializer

# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     def validate(self, attrs):
#         data = super().validate(attrs)

#         # refresh = self.get_token(self.user)

#         data["is_staff"] = str(self.user.is_staff)
#         # data["access"] = str(refresh.access_token)

#         return data


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserModel
        fields = "__all__"


class MyRegisterSerializer(RegisterSerializer):
    password2 = None
    password = serializers.CharField(write_only=True)
    password1 = password

    def validate(self, data):
        return data
