from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import Form, ModelForm

from .models import MyUserModel


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = MyUserModel
        fields = ["email", "username", "password1", "password2"]


# class UserLoginForm(Form):
#     email = forms.EmailField(required=True)
#     password1 = forms.CharField(max_length=65, widget=forms.PasswordInput)


class UserLoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(max_length=63, required=False)
    # class Meta:
    #     model = MyUserModel
    #     fields = ["email", "password"]

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password1")
        user_obj = MyUserModel.objects.filter(email=email).first()
        if not user_obj:
            raise forms.ValidationError("Sprawdź czy email i hasło są poprawne")
        else:
            if not user_obj.check_password(password):
                raise forms.ValidationError("Sprawdź czy email i hasło są poprawne")
        return super(UserLoginForm, self).clean(*args, **kwargs)
