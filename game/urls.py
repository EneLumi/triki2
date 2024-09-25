from django.urls import path
from . import views

# ühendab view-d ja netilehed
urlpatterns = [

    path("start/", views.start_quiz, name="start_quiz"),
    path("quiz/", views.play_game, name="play_game"),
    path("result/", views.result_view, name="result"),
    #path("rules/", views.rules, name="rules"),

]
