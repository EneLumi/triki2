from django.urls import path
from . import views

# ühendab view-d ja netilehed
urlpatterns = [

    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path("score_list/", views.score_list, name="score_list"),

]
