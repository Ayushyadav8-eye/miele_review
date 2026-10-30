
import re

from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["name", "mobile_number", "rating", "comment"]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your full name",
                "autocomplete": "name",
                "maxlength": "100",
            }),
            "mobile_number": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your mobile number",
                "autocomplete": "tel",
                "inputmode": "tel",
                "maxlength": "15",
            }),
            "rating": forms.Select(attrs={
                "class": "form-control",
            }),
            "comment": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Write your feedback here...",
                "rows": 5,
                "maxlength": "2000",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["rating"].choices = [
            ("", "Select your rating"),
            (1, "1 Star"),
            (2, "2 Stars"),
            (3, "3 Stars"),
            (4, "4 Stars"),
            (5, "5 Stars"),
        ]

        for field in self.fields.values():
            field.required = True

    def clean_name(self):
        name = self.cleaned_data["name"].strip()

        if not name:
            raise forms.ValidationError("Please enter your name.")

        return name

    def clean_mobile_number(self):
        mobile = self.cleaned_data["mobile_number"].strip()

        # Allow digits, spaces, +, parentheses and hyphens.
        if not re.fullmatch(r"[0-9+\s()-]+", mobile):
            raise forms.ValidationError(
                "Enter a valid mobile number."
            )

        digits = re.sub(r"\D", "", mobile)

        if not 10 <= len(digits) <= 15:
            raise forms.ValidationError(
                "The mobile number must contain 10 to 15 digits."
            )

        return mobile

    def clean_rating(self):
        rating = self.cleaned_data["rating"]

        if rating not in [1, 2, 3, 4, 5]:
            raise forms.ValidationError(
                "Please select a rating between 1 and 5."
            )

        return rating

    def clean_comment(self):
        comment = self.cleaned_data["comment"].strip()

        if not comment:
            raise forms.ValidationError(
                "Please enter your feedback."
            )

        return comment
