from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .forms import UserLoginForm, UserRegistrationForm


# Create your views here.
def register(request):
    form = UserRegistrationForm()
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")

    context = {"form": form, "action": "register"}
    return render(request, "user/loginRegister.html", context)


def login_user(request):
    form = UserLoginForm()
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Witaj @{user.get_username()}, ponownie!")
                return redirect("/")

    context = {"form": form, "action": "login"}
    return render(request, "user/loginRegister.html", context)
