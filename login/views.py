from django.shortcuts import render
from .forms import SignupForm

def index(request):
    return render(request, "login/index.html")

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = SignupForm()
    param = {"form": form}
    return render(request, "login/signup.html", param)