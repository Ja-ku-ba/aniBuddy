from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from pages.models import Post
from utils.orm import get_post, get_user_info
from .forms import UserLoginForm, UserRegistrationForm
from .models import MyUserModel


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
    return render(request, "user/pages/loginRegister.html", context)


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
    return render(request, "user/pages/loginRegister.html", context)


def logout_user(request):
    logout(request)
    return redirect("/")


def profile_page(request, pk):
    posts = get_post(Post, owner_id=pk)
    user = get_user_info(MyUserModel, pk)
    if not user:
        return messages.add_message(
            request, messages.ERROR, "Chcesz wyświetlić zaratość, która nie istnieje"
        )
    context = {"posts": posts, "user": user, "user_pk": pk}
    return render(request, "user/pages/userPage.html", context)
