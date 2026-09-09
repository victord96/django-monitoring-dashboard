from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from django_extensions.db.models import TimeStampedModel

from .managers import UserManager


class User(AbstractUser, TimeStampedModel):
    username = None
    email = models.EmailField(_("email address"), blank=False, null=False, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta(AbstractUser.Meta):
        ordering = ["-date_joined"]
