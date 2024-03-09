from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password):
        if not email:
            raise ValueError(_("Musisz podać adres email"))
        if not username:
            raise ValueError(_("Musisz podać nazwę użytkownika"))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password):
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class MyUserModel(AbstractUser):
    username = models.CharField(_("Nazwa użytkownika"), max_length=64, unique=True)
    email = models.EmailField(_("Email"), max_length=254, unique=True)
    account_created = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = MyUserManager()
