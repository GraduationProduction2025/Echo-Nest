from django import forms
from django.shortcuts import redirect, render
from .models import Survey

def index(request):
    surveys = Survey.objects.filter(delete_flag=False)  # 削除されていないSurveyを取得
    context = {
        'title': '質問一覧',
        'surveys': surveys,
    }
    return render(request, 'surveys/test.html', context)

# forms.pyに移行予定
SurveyFormSet = forms.modelformset_factory(Survey, fields=['id', 'title', 'url', 'create_at', 'create_user'], can_delete=True, extra=0)

def delete_surveys(request):
    queryset = Survey.objects.filter(delete_flag=False)  # 削除フラグが立っていないもののみ選択
    if request.method == 'POST':
        formset = SurveyFormSet(request.POST, queryset=queryset)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data.get('DELETE'):
                    survey = form.save(commit=False)
                    survey.delete_flag = True
                    survey.save()
            return redirect('templates:list')
    else:
        formset = SurveyFormSet(queryset=queryset)

    context = {
        'formset': formset,
    }

    return render(request, 'surveys/delete.html', context)