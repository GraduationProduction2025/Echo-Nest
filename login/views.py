from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import SignupForm, LoginForm
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return render(request, "login/index.html")

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="/login/")
    else:
        form = SignupForm()
    param = {"form": form}
    return render(request, "login/signup.html", param)

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                return redirect(to="/login/")
    else:
        form = LoginForm()
    param = {"form": form}
    return render(request, "login/login.html", param)

def logout_view(request):
    logout(request)
    return render(request, "login/logout.html")