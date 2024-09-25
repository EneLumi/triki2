from django.db import models
from django.contrib.auth.models import User


# ajutine salvestus, et skoori saada
class Question(models.Model):
    question_text = models.TextField()
    correct_answer = models.CharField(max_length=255)
    incorrect_answers = models.JSONField()  # ajutine fail

    def __str__(self):  #see osa pole hädavalik aga aitab tulemust paremini lugeda, paneb nö inimkeelde
        return self.question_text


# salvestab õige vastuse (ühe küsimuse kohta)
class QuizResult(models.Model):  # üks mitmele suhe, ühel küsimusel saab olla palju tulemusi
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # lingib iga tulemuse spetsiifilisele küsimusele
    user_choice = models.CharField(max_length=255)  # salvestab kasutaja valitud vastuse
    is_correct = models.BooleanField()  # kas vastus on õige või mitte

    def __str__(self):
        return f"{self.question} - {'Correct' if self.is_correct else 'Incorrect'}"


# salvestab kõik detailid, mis on vajalik skoori arvutamiseks
class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="scores")  # ühendab skoori kasutajaga, üks mitmele suhe
    difficulty = models.CharField(
        max_length=10,
        choices=[("Easy", "Easy"), ("Medium", "Medium"), ("Hard", "Hard")],
    )
    num_questions = models.PositiveSmallIntegerField()
    num_correct = models.PositiveSmallIntegerField()
    score = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self): #see osa on vajalik selleks, näidata skoori, kasutajat jne nö inimkeeles
        return (
            f"{self.user.username} - {self.score:.2f} points ({self.difficulty}, "
            f"{self.num_questions} questions, {self.num_correct} correct)"
        )

    class meta:
        ordering = [
            "-score"
        ]  # sisemine klass, mis ütleb, et skoor peaks olema andmebaasis kõrgemast madalamaks
