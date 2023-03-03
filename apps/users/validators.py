from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class CustomUsernameValidator(RegexValidator):
    regex = r"^[A-Za-z0-9_]+"
    message = _(
        "Username may contain only letters, digits and underscores."
    )
