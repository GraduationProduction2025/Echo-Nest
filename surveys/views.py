from django.shortcuts import render

def index(request):
    base = {
        'title':'質問一覧'
    }
    return render(request,'surveys/list_ques.html',base)
