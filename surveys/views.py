from django.shortcuts import render, get_object_or_404, redirect
from .models import Survey
from .forms import SurveyUpdateForm

def index(request):
    base = {
        'title':'質問一覧'
    }
    return render(request,'surveys/list_ques.html',base)

def list(request):
    survey = Survey.objects.all()
    base = {
        'title': '質問一覧',
        'surveys': survey,
    }
    return render(request, 'surveys/list_ques.html', base)

def update(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    if request.method == 'POST':
        form = SurveyUpdateForm(request.POST, instance=survey)
        if form.is_valid():
            form.save()
            return redirect('templates:list')
    else:
        form = SurveyUpdateForm(instance=survey)
    context = {
        'title': '質問の更新',
        'form': form
    }
    return render(request, 'surveys/update.html', context)