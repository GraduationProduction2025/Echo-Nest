from django.shortcuts import render,redirect
from .models import Survey, Question, Choice, Choicetype, Answer
from django.http import HttpResponse
from django.views.generic import TemplateView
from .forms import TextInputForm

# データベースを取得して表示する
def list_ques(request):
    survey_field_data = Survey.objects.values()
    listdict = {
        'title':'一覧',
        'val':survey_field_data,
    }
    return render(request, 'surveys/list_ques.html', listdict)

def create_ques(request):
    base = {
    'title':'アンケート作成'
    }
    return render(request,'surveys/create_ques.html',base)

def al_list(request):
    survey_field_data = Survey.objects.filter(published_flag=True)
    listdict = {
        'title':'公開済みアンケート一覧',
        'val':survey_field_data,
    }
    return render(request, 'surveys/al_list.html', listdict)

def tem_list(request):
    survey_field_data = Survey.objects.filter(published_flag=False)
    listdict = {
        'title':'下書きアンケート一覧',
        'val':survey_field_data,
    }
    return render(request, 'surveys/tem_list.html', listdict)

def ag_data(request, survey_id):
    survey_field_data = Survey.objects.get(id = survey_id)
    listdist = {
        'title':'集計結果',
        'val':survey_field_data
    }
    return render(request, 'surveys/ag_data.html', listdist)

def edit_ques(request, survey_id):
    survey = Survey.objects.get(id = survey_id)
    listdict = {
        'title':'編集画面',
        'survey':survey,
    }
    return render(request, 'surveys/edit_ques.html', listdict)

def answer(request, survey_id):
    survey = Survey.objects.get(id = survey_id)

    listdict = {
        'title':'回答画面',
        'survey':survey,
    }
    return render(request, 'answers/answer.html', listdict)

def complete(request):
    listdict = {
        'title' : '回答完了画面',
    }
    return render(request, 'answers/complete.html', listdict)
