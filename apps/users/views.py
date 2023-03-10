from django.utils.translation import gettext_lazy as _

from dj_rest_auth.app_settings import api_settings
from dj_rest_auth.jwt_auth import (CookieTokenRefreshSerializer,
                                   set_jwt_access_cookie, unset_jwt_cookies)
from dj_rest_auth.views import LogoutView as BaseLogoutView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView


class LogoutView(BaseLogoutView):
    def logout(self, request):
        response = Response(
            {"detail": _("Successfully logged out.")},
            status=status.HTTP_200_OK,
        )

        cookie_name = getattr(api_settings, "JWT_AUTH_REFRESH_COOKIE", None)

        unset_jwt_cookies(response)

        try:
            if cookie_name and cookie_name in request.COOKIES:
                token = RefreshToken(request.COOKIES.get(cookie_name))
                token.blacklist()
        except KeyError:
            response.data = {"detail": _(
                "Refresh token was not included in request cookies.")}
            response.status_code = status.HTTP_401_UNAUTHORIZED
        except (TokenError, AttributeError, TypeError) as error:
            if hasattr(error, "args"):
                if "Token is blacklisted" in error.args or "Token is invalid or expired" in error.args:
                    response.data = {"detail": _(error.args[0])}
                    response.status_code = status.HTTP_401_UNAUTHORIZED
                else:
                    response.data = {"detail": _("An error has occurred.")}
                    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            else:
                response.data = {"detail": _("An error has occurred.")}
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return response


class RefreshView(TokenRefreshView):
    serializer_class = CookieTokenRefreshSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code == 200 and "access" in response.data:
            set_jwt_access_cookie(response, response.data["access"])
            response.data = {"detail": _("Successfully refreshed token.")}
        return super().finalize_response(request, response, *args, **kwargs)
