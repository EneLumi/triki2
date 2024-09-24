from django.db import models
from django.contrib.auth.models import User

# salvestab kõik detailid, mis on vajalik skoori arvutamiseks
class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="scores") #ühendab skoori kasutajaga, üks mitmele suhe
    difficulty = models.CharField(
        max_length=10,
        choices=[("Easy", "Easy"), ("Medium", "Medium"), ("Hard", "Hard")],
    )
    num_questions = models.PositiveSmallIntegerField()
    num_correct = models.PositiveSmallIntegerField()
    score = models.DecimalField(max_digits=6, decimal_places=2)

    class meta:
        ordering = [
            "-score"
        ]  # sisemine klass, mis ütleb, et skoor peaks olema andmebaasis kõrgemast madalamaks
