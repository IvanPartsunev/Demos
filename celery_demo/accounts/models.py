from django.db import models

from celery_demo.accounts.managers import AccountManager
from celery_demo.accounts.mixins import CreatedOnEditedOnMixin
from django.contrib.auth import models as auth_models
from django.contrib.auth.models import AbstractUser


class AccountModel(CreatedOnEditedOnMixin, auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    class Roles(models.TextChoices):
        COUNTY_MANAGER = "CM", "Country Manager"
        DISTRICT_MANAGER = "DM", "District Manager"
        EMPLOYEE = "EMP", "Employee"

    email = models.CharField(
        max_length=255,
        unique=True,
        blank=False,
        null=False,
    )  # TODO: Get information what will be user for login

    role = models.CharField(
        choices=Roles.choices,
        default=Roles.EMPLOYEE,
        max_length=3,
        blank=False,
        null=False,
    )

    is_staff = models.BooleanField(
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )

    is_active = models.BooleanField(
        default=True,
        help_text="Designates whether this user should be treated as active. "
                  "Unselect this instead of deleting accounts."
    )

    objects = AccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["role"]

    def __str__(self):
        return self.email


class ProfileModel(CreatedOnEditedOnMixin):
    first_name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
    )

    second_name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
    )

    last_name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
    )

    account = models.OneToOneField(
        AccountModel,
        on_delete=models.CASCADE,
    )

    @property
    def get_full_name(self):
        if not self.first_name or not self.last_name:
            return "Name not entered. Update profile."
        full_name = f"{self.first_name} {self.second_name} {self.last_name}"
        return full_name.strip()
