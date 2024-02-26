from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'pages/home.html')

def addPost(request, page):
    return render(request, 'pages/add.html')