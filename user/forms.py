from django.contrib.auth.forms import UserCreationForm

from .models import MyUserModel


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = MyUserModel
        fields = ["email", "username", "password1", "password2"]
