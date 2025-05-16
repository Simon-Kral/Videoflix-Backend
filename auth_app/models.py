from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """
    Custom user model that replaces the username field with email as the unique identifier.
    Uses CustomUserManager to handle user creation and authentication.
    """
    username = None
    email = models.EmailField(_("email address"), unique=True)
    is_active = models.BooleanField(default=False)

    # Use the custom user manager for creating users and superusers.
    objects = CustomUserManager()

    # Set email as the primary field for authentication.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        # Return the user's email as the string representation.
        return self.email
