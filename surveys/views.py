from django.shortcuts import render
from .models import Survey, Question, Choice, Choicetype
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
    header = ['ステータス','質問タイトル','作成日','作成ユーザ']
    infodict = {
        'title':'テスト',
        'header':header,
        'val':survey,
        'val2':survey_2,
    }
    return render(request, 'surveys/info.html', infodict)

# データベースの内容を取得して表示
def detail(request):
    survey = Survey.objects.all()
    question = Question.objects.all()
    choicetype = Choicetype.objects.all()
    choice = Choice.objects.all()
    header = ['ステータス','質問タイトル','URL','作成日','作成ユーザ']
    detaildict = {
        'title':'アンケート詳細',
        'header':header,
        'survey':survey,
        'q':question,
        'c':choice,
        'ct':choicetype,
    }
    return render(request, 'surveys/detail.html', detaildict)

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