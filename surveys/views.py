from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic import TemplateView

# データベースを取得して表示する
def list(request):
    # header = ['ステータス','質問タイトル','URL','作成日','作成ユーザ']
    header = ['ステータス','質問タイトル','作成日','作成ユーザ','詳細']
    listdict = {
        'title':'テスト',
        'header':header,
    }
    return render(request, 'answer/list_ques.html', listdict)

# データベースの内容を取得して表示
def detail(request, survey_id):
    return render(request, 'answer/detail.html')

# テスト
def add(request):
    base = {
        'title':'アンケート追加'
    }
    return render(request,'answer/add.html',base)
    # return HttpResponse('add')

def create(request):
    base = {
    'title':'アンケート作成'
    }
    return render(request,'answer/create.html',base)
    # return HttpResponse('create')

def ans(request):
    base = {
    'title':'回答画面'
    }
    return render(request,'answer/sample.html',base)
    # return HttpResponse('create')

def fin(request):
    base = {
    'title':'回答完了'
    }
    return render(request,'answer/fin_answer.html',base)
    # return HttpResponse('create')