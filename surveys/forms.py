from django import forms

class TextInputForm(forms.Form):
    survey_id = forms.IntegerField(widget=forms.HiddenInput())