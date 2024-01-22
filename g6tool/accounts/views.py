from django.views.generic import RedirectView
from dj_rest_auth.registration.views import RegisterView
from rest_framework.response import Response
from rest_framework import status
from dj_rest_auth.jwt_auth import set_jwt_cookies


from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView


class GoogleLogin(
    SocialLoginView
):  # if you want to use Authorization Code Grant, use this
    adapter_class = GoogleOAuth2Adapter
    callback_url = "https://chatg6.ai/api/auth/callback/google"
    client_class = OAuth2Client


# https://accounts.google.com/o/oauth2/v2/auth?redirect_uri=http://localhost:3000/api/auth/callback/google&prompt=consent&response_type=code&client_id=46506568764-mmskn93aiuqaqunupfcllc0kia8pqd29.apps.googleusercontent.com&scope=openid%20email%20profile&access_type=offline


class SignUpView(RegisterView):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = self.get_response_data(user)

        if data:
            data["refresh"] = ""
            response = Response(
                data,
                status=status.HTTP_201_CREATED,
                headers=headers,
            )
            set_jwt_cookies(response, self.access_token, self.refresh_token)
            print("||||||||" + str(response.cookies))
        else:
            response = Response(status=status.HTTP_204_NO_CONTENT, headers=headers)

        return response


class RediredtOnVerifyView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        token = kwargs.get("token", None)
        uid = kwargs.get("uid", None)
        if uid and token:
            url = f"{self.url}/password/reset/confirm/{uid}/{token}"
        elif token:
            url = f"{self.url}/email/verify/{token}"
        else:
            url = f"{self.url}"

        print(f"args:{url}")
        print(f"args:{kwargs}")
        print(f"args:{self.kwargs}")
        return url
