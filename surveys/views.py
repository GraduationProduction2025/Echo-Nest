from django.shortcuts import render, redirect
from .models import Survey, Question, Choice, Choicetype
from django.utils import timezone
from django.db import models
import re

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

        # ques-title フィールド名をすべて取得してリストに追加
        for key, value in request.POST.items():
            if re.match(r'^ques-title-\d+$', key):
                question_titles.append(value)

        # タイトルとタイプの数が一致しない場合のエラーハンドリング
        if len(question_titles) != len(question_types):
            raise ValueError("質問タイトルと質問タイプの数が一致しません")

        # 各質問を保存
        for i in range(len(question_titles)):
            max_question_id = Question.objects.aggregate(models.Max('id'))['id__max'] or 0
            new_question_id = max_question_id + 1

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

            # チェックボックスの場合にのみ選択肢を取得
            if question_type_id == 2:
                choice_texts = []
                option_index = 1
                while True:
                    choice_key = f'option-text-{i + 1}-{option_index}'
                    choice_text = request.POST.get(choice_key)
                    if not choice_text:
                        break
                    choice_texts.append(choice_text.strip())
                    option_index += 1

                # 各選択肢を保存
                for choice_text in choice_texts:
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

