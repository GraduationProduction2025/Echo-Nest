from django import forms
from .models import Survey

class SurveyDelForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['id', 'title', 'url', 'create_at', 'create_user', 'delete_flag']
