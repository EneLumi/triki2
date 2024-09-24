from typing import Any
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


# lisab nime, perekonnanime, e-maili juba sisseehitatud süsteemile
class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        label="",  # kasti pealkiri, praegu tühi
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Email Address"}
            # form-control (bootstrap) kasutab sisseehitaud css-i, placeholder (kasti sees abitekst, halliga kirjutatud)
        ),
    )
    first_name = forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "First Name"}
        ),
    )
    last_name = forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Last Name"}
        ),
    )

    # vajalik databaasi jaoks, info ja veergude pealkirjad, mis peaks kindlasti olemas olema
    class Meta:
        model = User  # sisseehitatud
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "password1",
            "password2",
        ]

    # loob konteineri koos sisuga
    def __init__(self, *args: Any, **kwargs: Any):
        super(RegisterForm, self).__init__(*args, **kwargs)
        # võtab ülevalt (rida 8) klassist lisad ja paneb kokku praegusega, et teha õige form

        self.fields["username"].widget.attrs["class"] = "form-control"  # username kast ise
        self.fields["username"].widget.attrs["placeholder"] = "Username"  # näen kastis sees
        self.fields["username"].label = ""  # kasti pealkiri (üleval) puudub
        self.fields["username"].help_text = (
            '<span class="form-text text-muted"><small>Required. 150 characters or fewer. '
            'Letters, digits and @/./+/-/_ only.</small>'
        )  # lisatekst lehel näha

        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["placeholder"] = "Password"
        self.fields["password1"].label = ""
        self.fields["password1"].help_text = (
            "<ul class=\"form-text text-muted small\">"
            "Your password can't be too similar to your other personal information."
            "<br>"
            "Your password must contain at least 8 characters.<br>Your password can't be a commonly used password."
            "<br>"
            "Your password can't be entirely numeric."
            "</ul>"
        )
        self.fields["password2"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["placeholder"] = "Confirm Password"
        self.fields["password2"].label = ""
        self.fields["password2"].help_text = (
            "<small>Your password confirmation won't be shown, but you'll be able to view it as you type.</small>"
        )
