from datetime import datetime

from django.shortcuts import render, redirect

from .forms import PostForm
from .models import Post

# Create your views here.
def home(request):
    return render(request, 'pages/home.html')

def add(request, page):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            Post.objects.create(
                description = request.POST.get('description'),
                content = request.POST.get('content'),
                added = datetime.now()
            )
            return redirect('home')
    context = {'form': form}
    return render(request, 'pages/add.html', context)