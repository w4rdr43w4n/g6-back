from django.urls import path
from .views import RediredtOnVerifyView, GoogleLogin
from dj_rest_auth.views import (
    LoginView,
    LogoutView,
    UserDetailsView,
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetView,
)
from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.registration.views import (
    VerifyEmailView,
    ResendEmailVerificationView,
    RegisterView,
)
from .views import SignUpView
from django_main.settings import CURRENT_ORIGIN

urlpatterns = [
    # api/v1/auth/registration/
    path("google/", GoogleLogin.as_view(), name="google_login"),
    path(
        # the url sent in the verification email
        "account-confirm-email/<token>",
        RediredtOnVerifyView.as_view(url=CURRENT_ORIGIN),
        name="account_confirm_email",
    ),
    path(
        "password/reset/confirm/<uid>/<token>",
        RediredtOnVerifyView.as_view(url=CURRENT_ORIGIN),
        name="password_reset_confirm",
    ),
    path("registration/signup", SignUpView.as_view(), name="rest_register"),
    path(
        "registration/verify-email", VerifyEmailView.as_view(), name="rest_verify_email"
    ),
    path(
        "registration/resend-email",
        ResendEmailVerificationView.as_view(),
        name="rest_resend_email",
    ),
    # api/v1/auth/login/ [name='rest_login']
    path("login", LoginView.as_view(), name="rest_login"),
    path(
        "password/reset/confirm",
        PasswordResetConfirmView.as_view(),
        name="rest_password_reset_confirm",
    ),
    path("password/reset", PasswordResetView.as_view(), name="rest_password_reset"),
    path("password/change", PasswordChangeView.as_view(), name="rest_password_change"),
    path("user", UserDetailsView.as_view(), name="rest_user_details"),
    path("logout", LogoutView.as_view(), name="rest_logout"),
    path("token/refresh", get_refresh_view().as_view(), name="token_refresh"),
]
