from django.urls import path, include
from . import views

# ühendab view-sid ja html-e
urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register_user, name="register"),
    #path("", include("game.urls")), # ütleb djangole, et ta vaataks ka game app-is olevad urls faile
]
