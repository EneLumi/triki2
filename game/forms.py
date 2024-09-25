from django import forms
from .utils import get_categories, get_difficulties
from .models import Score


# kujundab tabelid
class QuizSettingsForm(forms.Form):
    category = forms.ChoiceField(choices=get_categories(), label="Category") #kategooriate valikud genereeritakse get_categories funktsiooniga
    amount = forms.IntegerField(
        label="Number of Questions",
        min_value=5,
        max_value=25,
        widget=forms.NumberInput(attrs={"type": "range", "step": 5}), #küsimuste arvu valiku slider
    )
    difficulty = forms.ChoiceField(choices=get_difficulties(), label="Difficulty")


# mängu enda form
class QuizForm(forms.Form): #mitte lingitud mudelite külge (muidu oleks Model.Form)
    choice = forms.ChoiceField(widget=forms.HiddenInput(), label="") #hiddenInput tähendab, et kasutaja ei näe aga mäng ikka arvestab

    def __init__(self, *args, **kwargs): # init on klassi konstruktor,
        choices = kwargs.pop("choices") #choises key eemaldatakse kwargs-idest, et seda ei antaks edasi
        super().__init__(*args, **kwargs) #super kutsub meetodit parent classist (init meetodit)
        self.fields["choice"].choices = choices


# tulemuste form
class ScoreForm(forms.ModelForm): #ModelForm tähendab, et on lingitud otse models külge
    class Meta:
        model = Score #näitab, et on lingitud Score models külge
        fields = ("difficulty", "num_questions", "num_correct", "score") #ütleb millised väljad models-ist peaks olema lisatud formile

