from django.shortcuts import render
from .models import Survey

def index(request):
    base = {
        'title':'質問一覧'
    }
    return render(request,'surveys/list_ques.html',base)

# データベースを取得して表示する
def info(request):
    survey = Survey.objects.all()
    survey_2 = Survey.objects.values()
    infodict = {
        'title':'テスト',
        'val':survey,
        'val2':survey_2,
    }
    return render(request, 'surveys/list.html', infodict)