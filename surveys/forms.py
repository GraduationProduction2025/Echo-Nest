from django import forms
from .models import Survey

class SurveyUpdateForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['title', 'url', 'create_user',]
