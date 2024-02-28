from datetime import datetime

from django.shortcuts import redirect, render

from .forms import PostForm
from .models import Post


# Create your views here.
def home(request):
    return render(request, "pages/home.html")


def add(request, page):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = Post.objects.create(
                description=request.POST.get("description"),
                content=request.POST.get("content"),
                added=datetime.now(),
            )
            images = request.FILES.getlist("images")
            for image in images:
                new_post.image = image
                new_post.save()
            return redirect("home")
        # else:
        # var = dir(form.errors.items())
        # print(var)
        # print(form.errors.get_json_data()["__all__"][0]["message"])
    context = {"form": form}
    return render(request, "pages/add.html", context)
