from django import forms


class CheckInForm(forms.Form):
    query = forms.CharField(
        label="Name or Invitation Code",
        max_length=120,
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-4 py-3 pr-12 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 text-gray-700 placeholder-gray-400",
                "placeholder": "Invitation Code",
            }
        ),
    )
