from allauth.account import app_settings
from allauth.account.adapter import DefaultAccountAdapter
from allauth.utils import import_attribute


class CustomAccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        url = f"http://localhost:8080/signup/emailconfirm/{emailconfirmation.key}"
        return url


def get_adapter(request=None):
    return import_attribute(app_settings.ADAPTER)(request)
