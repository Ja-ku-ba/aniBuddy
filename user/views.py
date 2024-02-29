from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .forms import UserRegistrationForm


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

    context = {"form": form}
    return render(request, "user/loginRegister.html", context)
