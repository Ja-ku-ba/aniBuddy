from datetime import datetime

from django.contrib import messages
from django.shortcuts import redirect, render

from base.settings import MEDIA_ROOT, MEDIA_URL

from .forms import PostForm, PostImageForm
from .models import Post, PostImage


# Create your views here.
def home(request):
    # room = Room.objects.get(id=pk)
    # room_messages = room.message_set.all()
    posts = Post.objects.all()
    images = posts.postImages_set.all()
    print(images)
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
