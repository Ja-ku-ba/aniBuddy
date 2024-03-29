from datetime import datetime

from django.contrib import messages
from django.shortcuts import redirect, render
from filetype import guess

from user.models import MyUserModel
from utils.orm import get_post, get_messages_headers, get_messages_from_chat
from .forms import ComentForm, PostForm, PostImageForm
from .models import Coment, Post, PostImage, Reaction


# Create your views here.
def home(request):
    posts = get_post(Post)

    context = {"posts": posts}
    return render(request, "pages/home.html", context)


def post_add(request):
    form = PostForm()
    formImages = PostImageForm()

    if request.method == "POST":
        form = PostForm(request.POST)
        formImages = PostImageForm(request.POST, request.FILES)

        # chcek if user want to add an empty post
        if form.is_valid() and formImages.is_valid():
            if not any([form.clean(), formImages.clean()]):
                messages.add_message(
                    request,
                    messages.ERROR,
                    "Co najmniej jedno pole musi zawierać wartość",
                )
                return redirect("poast_add")

            # chcek if files are images/gifs, not other types
            # before any crud on db (eg. Post)
            images = request.FILES.getlist("image")
            for file in images:
                kind = guess(file)
                # if file is diffrent format than image/gif, then throw error
                # if format is None, throw error
                try:
                    if not kind.mime.startswith("image"):
                        raise KeyError
                except:
                    messages.add_message(
                        request, messages.ERROR, "Przesłany plik nie jest zdjęciem."
                    )
                    return redirect("poast_add")

            # creates a new post object
            new_post = Post.objects.create(
                owner=request.user,
                description=request.POST.get("description"),
                content=request.POST.get("content"),
                added=datetime.now(),
            )

            # saves images related to post
            for request_image in images:
                new_image = PostImage.objects.create(post=new_post)
                new_image.save()
                new_image.image = request_image
                new_image.save()

            return redirect("home")
    context = {"form": form, "formImages": formImages}
    return render(request, "pages/addPost.html", context)


def post_page(request, pk):
    form = ComentForm()

    if request.method == "POST":
        form = ComentForm(request.POST)
        if form.is_valid():
            Coment.objects.create(
                post_id=pk,
                coment=request.POST.get("coment"),
                added=datetime.now(),
                owner=request.user,
            )
        else:
            if len(request.POST.get("coment")) > 1023:
                messages.add_message(
                    request,
                    messages.INFO,
                    "Możesz napisać komentarz składający się tylko 1000 zanków",
                )
        return redirect("post_page", pk)

    try:
        reaction = Reaction.objects.get(post_id=pk, user=request.user).reaction
    except:
        # if user does not interacted with post yet
        reaction = 0

    try:
        post = get_post(Post, id=pk)
        coments = Coment.objects.filter(post_id=pk)
        images = PostImage.objects.filter(post_id=pk)

        context = {
            "post": post[0],
            "form": form,
            "coments": coments,
            "reaction_status": reaction,
            "images": images,
        }
    except:
        messages.add_message(
            request, messages.ERROR, "Chcesz wyświetlić zawartość, która nie istnieje."
        )
        return redirect("home")

    return render(request, "pages/postView.html", context)


def post_delete(request, pk):
    try:
        post = Post.objects.get(id=pk, owner=request.user)
    except:
        messages.error(
            request,
            "Chcesz usunąć post, którego nie jesteś w posiadaniu.",
        )
        return redirect("home")
    post.delete()
    return redirect("home")


def add_interaction(request, pk):
    if request.method == "POST":
        try:
            action = int(request.POST.get("reaction"))
        except TypeError:
            action = None

        try:
            # if user want to change from dislike to like
            reaction = Reaction.objects.get(post_id=pk, user=request.user)

            if action in [-1, 1]:
                # ensure that user wants to unlike or undislike
                if reaction.reaction != action:
                    Reaction.objects.create(
                        post_id=pk, user=request.user, reaction=action
                    ).save()
                reaction.delete()
            else:
                raise ValueError
        except:
            # first user interaction with post
            if action in [-1, 1]:
                Reaction.objects.create(
                    post_id=pk, user=request.user, reaction=action
                ).save()
                return redirect("post_page", pk)
            messages.add_message(
                request,
                messages.ERROR,
                "Interakcja, którą chcesz przeprowadzić jest nie możliwa",
            )
    return redirect("post_page", pk)


def messages_page(request):
    messages_headers = get_messages_headers(request.user.id)
    context = {"headers": messages_headers}
    return render(request, "pages/messagePage.html", context)


def send_message_page(request, pk1, pk2):
    if pk1 == request.user.id:
        chat_messages = get_messages_from_chat(pk1, pk2)
        second_user_pk = pk2
    else:
        chat_messages = get_messages_from_chat(pk2, pk1)
        second_user_pk = pk1

    try:
        roommate = MyUserModel.objects.get(id=second_user_pk)
    except ValueError:
        messages.add_message(
            request, messages.ERROR, "Chcesz wyświetlić rozmowę, która nie istnieje"
        )
        return redirect("messages")

    context = {"chat_messages": chat_messages, "roommate_username": roommate.username}
    return render(request, "pages/chat.html", context)
