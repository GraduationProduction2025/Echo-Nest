from django.shortcuts import render, redirect
from .models import Survey, Question, Choice, Choicetype
from django.utils import timezone
from django.db import models

# データベースを取得して表示する
def list(request):
    survey = Survey.objects.all()
    survey_2 = Survey.objects.values()
    # header = ['ステータス','質問タイトル','URL','作成日','作成ユーザ']
    header = ['ステータス','質問タイトル','作成日','作成ユーザ','詳細']
    listdict = {
        'title':'テスト',
        'header':header,
        'val':survey,
        'val2':survey_2,
    }
    return render(request, 'surveys/list_ques.html', listdict)

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

def create_ques(request):
    # GETリクエストの場合、入力フォームを表示
    choicetypes = Choicetype.objects.all()  # 質問タイプを選ぶために全てのタイプを取得
    # base辞書を作成
    base = {
        'title': 'アンケート作成',
        'choicetypes': choicetypes,  # 質問タイプを追加
    }
    survey = Survey.objects.all()
    survey_2 = Survey.objects.values()
    # header = ['ステータス','質問タイトル','URL','作成日','作成ユーザ']
    header = ['ステータス','質問タイトル','作成日','作成ユーザ','詳細']
    listdict = {
        'title':'テスト',
        'header':header,
        'val':survey,
        'val2':survey_2,
    }

    if request.method == 'POST' and request.POST.get('action') == 'create':
        print("POSTデータ:", request.POST)
        # Surveyモデルの最大IDを取得
        max_survey_id = Survey.objects.aggregate(models.Max('id'))['id__max'] or 0
        new_survey_id = max_survey_id + 1

        survey_title = request.POST.get('title-text')
        survey_url = "http://example.com/"
        survey_create_user = "admin"

        # 新しいSurveyオブジェクトを作成
        survey = Survey(
            id=new_survey_id,
            title=survey_title,
            url=survey_url,
            create_at=timezone.now(),
            create_user=survey_create_user,
            delete_flag=False
        )
        survey.save()

        # 質問と選択肢を処理
        question_titles = request.POST.getlist('ques-title')
        question_types = request.POST.getlist('ques-type')

        for i in range(len(question_titles)):
            max_question_id = Question.objects.aggregate(models.Max('id'))['id__max'] or 0
            new_question_id = max_question_id + 1

            # 適切な選択肢タイプを取得
            question_type_id = int(question_types[i])  # 1がtextbox、2がcheckbox
            question_type = Choicetype.objects.get(id=question_type_id)

            # Questionオブジェクトの作成
            question = Question(
                id=new_question_id,
                title=question_titles[i],
                survey=survey,
                type=question_type
            )
            question.save()

            # チェックボックスタイプの場合のみ選択肢を取得
            if question_type_id == 2:  # チェックボックスの場合
                # インデックスに基づくキー名を使用
                choice_texts = request.POST.getlist(f'option-text-{i}')  # インデックスを使用して選択肢を取得

                for choice_text in choice_texts:
                    choice_text = choice_text.strip()
                    if choice_text:
                        max_choice_id = Choice.objects.aggregate(models.Max('id'))['id__max'] or 0
                        new_choice_id = max_choice_id + 1

                        choice = Choice(
                            id=new_choice_id,
                            text=choice_text,
                            question=question
                        )
                        choice.save()

        return render(request, 'surveys/list_ques.html', listdict)

    return render(request, 'surveys/create_ques.html', base)

