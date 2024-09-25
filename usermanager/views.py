from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from usermanager.forms import RegisterForm


# annan käskluse, mida näha netilehel
def home(request):
    return render(request, "home.html", {})


# suunab sisselogimise lehele ja küsib kasutajatunnust ja salasõna
def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You are now logged in")
            return redirect("home")
        messages.error(request, "There was an error logging in. Please try again")
        return redirect("login")
    return render(request, "login.html", {})


# fuktsionaalsus väljalogimiseks, läheb algsele lehele
def logout_user(request):
    logout(request)
    messages.success(request, "You are now logged out")
    return redirect("home")


# suunab registreerimise lehele ja registreerib kasutaja
def register_user(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully registered")
            return redirect("home")
    form = RegisterForm()
    return render(request, "register.html", {"form": form})
