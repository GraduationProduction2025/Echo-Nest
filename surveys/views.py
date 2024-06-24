from django.shortcuts import render,redirect
from .models import Survey, Question, Choice, Choicetype
from django.http import HttpResponse
from django.views.generic import TemplateView

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
    questions = Question.objects.filter(survey=survey)
    choices = Choice.objects.filter(question__in=questions)
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

def detail_view(request):
    # ヘッダー行の登録
    sheader = ['アンケートID','アンケートタイトル','URL','作成日','作成ユーザ','削除フラグ']
    ctheader = ['タイプID','タイプ']
    qheader = ['質問ID','質問タイトル','アンケートID','タイプID']
    cheader = ['選択肢ID','テキスト','質問ID']
    # データを取得
    survey = Survey.objects.all()
    question = Question.objects.all()
    choicetype = Choicetype.objects.all()
    choice = Choice.objects.all()
    context = {
        'sh': sheader,
        'cth': ctheader,
        'qh': qheader,
        'ch': cheader,
        's': survey,
        'q': question,
        'ct':choicetype,
        'c':choice,
    }
    
    return render(request, 'surveys/detail.html', context)

def test(request):
    # header最終形
    # header = ['ID','アンケートタイトル','質問タイトル','タイプ','テキスト']
    # surveys.id, surveys.title, question.title, choicetype.type, choice.text
    header = ['question.title', 'choice.text']  
    choice = Choice.objects.get(id=1)
    data = choice.question.title
    queryset = Question.objects.select_related('survey_id').values()
    queryset2 = Question.objects.select_related('survey_id').only()
    cset = Choice.objects.select_related('question_id').values()
    data2 = Question.objects.filter(id=1)
    dict=[]
    for i in queryset:
        dict=i

    # データを取得
    # survey = Survey.objects.all()
    # question = Question.objects.all()
    # choicetype = Choicetype.objects.all()
    # choice = Choice.objects.all()
    # SQLを記述
    # data = Question.objects.prefetch_related(survey).get(id=1)
    
    base={
    'title': 'テスト',
    'header': header,
    'data': data,
    'qset': queryset,
    'oset': queryset2,
    'data2': data2,
    'dict': dict,
    'cset': cset,
    }
    return render(request, 'surveys/test.html', base)