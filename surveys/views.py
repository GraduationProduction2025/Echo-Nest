from django.shortcuts import render, redirect
from .models import Survey, Question, Choice, Choicetype, Answer
from django.http import HttpResponse, Http404
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db import models
import re

# データベースを取得して表示する
def list_ques(request):
    survey_field_data = Survey.objects.values()
    listdict = {
        'title':'一覧',
        'val':survey_field_data,
    }
    return render(request, 'surveys/list_ques.html', listdict)

def create_ques(request):
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

    return render(request, 'surveys/create_ques.html', listdict)


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
    try:
        # ページ番号と同じSurveyを取り出す
        survey = Survey.objects.get(id=survey_id)
        # 上のアンケートに関連したQuestionを取り出す
        question = Question.objects.filter(survey__id = survey_id)
        listdict = {
            "survey": survey,
            "question": question,
            "title": survey.title,
        }
    except Survey.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, "answers/answer.html", listdict)

@csrf_exempt  # CSRF保護を一時的に無効にする（開発中のみ）
def complete(request):
    if request.method == 'POST':
        responses = request.POST
        response_list = []

        for key, value in responses.items():
            if key != 'csrfmiddlewaretoken':
                question_id = int(key)
                question = Question.objects.get(id=question_id)  # 質問を取得
                answer_data = {
                    "question_id": question.id,  # 質問のIDを取得
                    "type": str(question.type),  # 質問のタイプを取得
                    "content": [value],  # ユーザーが入力した回答をリスト形式で格納
                }

                # Answerインスタンスを作成
                answer_instance = Answer(
                    context=answer_data,  # JSONデータをcontextに格納
                    question=question  # Questionを関連付け
                )
                answer_instance.save()  # データベースに保存
                response_list.append(answer_data)
        listdict = {
            'title': '回答完了画面',
            'responses': response_list,
        }        
        return render(request, 'answers/complete.html', listdict)

    return render(request, 'answers/answer.html', {'title': '回答ページ'})