from django import forms

class BotForm(forms.Form):
    image_value = forms.FileField()