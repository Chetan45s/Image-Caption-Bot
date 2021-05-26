from django import forms

class LangForm(forms.Form):
    expr = forms.CharField()