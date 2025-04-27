from django import forms


class CheckInForm(forms.Form):
    query = forms.CharField(
        label="Name or Invitation Code",
        max_length=120,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Invitation Code",
            }
        ),
    )
