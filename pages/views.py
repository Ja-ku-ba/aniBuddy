from datetime import datetime

from django.contrib import messages
from django.shortcuts import redirect, render

from base.settings import MEDIA_ROOT, MEDIA_URL

from .forms import PostForm
from .models import Post


# Create your views here.
def home(request):
    posts = Post.objects.all()
    context = {"posts": posts}
    print(MEDIA_ROOT)
    print(MEDIA_URL + "posts/2023-06-13_1232570000.png")
    return render(request, "pages/home.html", context)


def add(request, page):
    form = PostForm()

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = Post.objects.create(
                owner=request.user,
                description=request.POST.get("description"),
                content=request.POST.get("content"),
                added=datetime.now(),
            )
            images = request.FILES.getlist("images")
            for image in images:
                new_post.image = image
                new_post.save()
            return redirect("home")
    context = {"form": form}
    return render(request, "pages/add.html", context)


def post_page(request, id):
    return render(request, "pages/postView.html")


def delete_post(request, id):
    try:
        post = Post.objects.get(id=id, owner=request.user)
    except:
        messages.error(
            request,
            "Chcesz usunąć post, którego nie jesteś w posiadaniu.",
        )
        return redirect("home")
    post.delete()
    return redirect("home")
