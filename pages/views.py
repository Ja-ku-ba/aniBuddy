from datetime import datetime

from django.contrib import messages
from django.db.models import Count, Min, Value
from django.db.models.functions import Concat
from django.shortcuts import redirect, render

from base.settings import MEDIA_ROOT, MEDIA_URL

from .forms import PostForm, PostImageForm
from .models import Post, PostImage

# from .orm import get_post_image


# Create your views here.
def home(request):

    # is used to specify if post have image, if do then, get how many,
    # then get first image path
    posts = (
        Post.objects.annotate(
            images_quantity=Count("postimage__post_id", distinct=True),
            image_first=Min("postimage__image"),
            image_first_id=Min("postimage__id"),
            username=Concat("owner__username", Value("")),
        )
        .order_by("-added")
        .values(
            "id",
            "added",
            "owner",
            "username",
            "content",
            "description",
            "images_quantity",
            "image_first",
            "image_first_id",
        )
    )
    for x in posts:
        print(x)
    context = {"posts": posts}
    print(MEDIA_ROOT)
    print(MEDIA_URL + "posts/2023-06-13_1232570000.png")
    return render(request, "pages/home.html", context)


def post_add(request):
    form = PostForm()
    formImages = PostImageForm()
    if request.method == "POST":
        formPost = PostForm(request.POST)
        formImages = PostImageForm(request.POST, request.FILES)
        if formPost.is_valid() and formImages.is_valid():
            # creates a new post object
            new_post = Post.objects.create(
                owner=request.user,
                description=request.POST.get("description"),
                content=request.POST.get("content"),
                added=datetime.now(),
            )

            # saves images related to post
            images = request.FILES.getlist("images")
            for request_image in images:
                new_image = PostImage.objects.create(post=new_post)
                new_image.save()
                new_image.image = request_image
                new_image.save()

            return redirect("home")
    context = {"form": form, "formImages": formImages}
    return render(request, "pages/addPost.html", context)


def post_page(request, id):
    return render(request, "pages/postView.html")


def post_delete(request, id):
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
