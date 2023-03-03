from django.urls import path, re_path

from dj_rest_auth.registration.views import RegisterView, VerifyEmailView
from dj_rest_auth.views import LoginView

from .views import LogoutView, RefreshView

urlpatterns = [
    path("token/", LoginView.as_view(), name="jwt_token"),
    path("token/refresh/", RefreshView.as_view(), name="jwt_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),

    path("register/", RegisterView.as_view(), name="register"),
    re_path(r"^account-confirm-email/", VerifyEmailView.as_view(),
            name="account_email_verification_sent"),
    re_path(r"^account-confirm-email/(?P<key>[-:\w]+)/$",
            VerifyEmailView.as_view(), name="account_confirm_email"),
]
