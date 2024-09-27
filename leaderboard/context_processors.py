from game.models import Score

# et näitaks koguaeg, olen sisse logitud või mitte (sidebar-il). Lisafunktsioon, mis koguaeg jookseb ja kõigil templatidel (live)
def leaderboard_context(request):
    scores = Score.objects.order_by('-score')[:30]
    user_scores = Score.objects.filter(user=request.user).order_by('-score') \
        if request.user.is_authenticated else []
    return {
        'scores': scores,
        'user_scores': user_scores,
    }
