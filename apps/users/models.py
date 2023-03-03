from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .validators import CustomUsernameValidator


class CustomUser(AbstractUser):
    username_validator = CustomUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=30,
        unique=True,
        help_text=_(
            "Username may contain only letters, digits or underscores. No more than 30 characters."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("Username is already taken.")
        }
    )
    email = models.EmailField(
        "email address",
        unique=True,
        blank=True
    )
