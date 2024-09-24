from django.db import models

# ajutine salvestus, et skoori saada
class Question(models.Model):
    question_text = models.TextField()
    correct_answer = models.CharField(max_length=255)
    incorrect_answers = models.JSONField()  # ajutine fail


# salvestab õige vastuse (ühe küsimuse kohta)
class QuizResult(models.Model): # üks mitmele suhe, ühel küsimusel saab olla palju tulemusi
    question = models.ForeignKey(Question, on_delete=models.CASCADE) # lingib iga tulemuse spetsiifilisele küsimusele
    user_choice = models.CharField(max_length=255) #salvestab kasutaja valitud vastuse
    is_correct = models.BooleanField() #kas vastus on õige või mitte
