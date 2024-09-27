from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from game.models import Score



# leaderboardi lehele viide
def leaderboard(request):
    scores = Score.objects.order_by("-score")
    return render(request, "leaderboard.html", {"scores": scores})


@login_required
def score_list(request):
    scores = Score.objects.filter(user=request.user).order_by("-score")
    return render(request, "score_list.html", {"user_scores": scores})



