from django.shortcuts import render
from .models import Survey, Question, Choice
from django.http import HttpResponse

def index(request):
    base = {
        'title':'質問一覧'
    }
    return render(request,'surveys/list_ques.html',base)

# データベースを取得して表示する
def info(request):
    survey = Survey.objects.all()
    survey_2 = Survey.objects.values()
    # header = ['ステータス','質問タイトル','URL','作成日','作成ユーザ']
    header = ['ステータス','質問タイトル','作成日','作成ユーザ','詳細']
    infodict = {
        'title':'テスト',
        'header':header,
        'val':survey,
        'val2':survey_2,
    }
    return render(request, 'surveys/info.html', infodict)

# データベースの内容を取得して表示
def detail(request, survey_id):
    survey = Survey.objects.get(id=survey_id)
    questions = Question.objects.filter(survey_id=survey)
    choices = Choice.objects.filter(question_id__in=questions)
    context = {
        'survey': survey,
        'questions': questions,
        'choices': choices,
    }
    return render(request, 'surveys/detail.html', context)

# テスト
def add(request):
    base = {
        'title':'アンケート追加'
    }
    return render(request,'surveys/add.html',base)
    # return HttpResponse('add')

def create(request):
    base = {
    'title':'アンケート作成'
    }
    return render(request,'surveys/create.html',base)
    # return HttpResponse('create')