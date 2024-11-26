from django.shortcuts import render, redirect
from .models import Survey, Question, Choice, Choicetype, Answer
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import re
from django.contrib.auth.decorators import login_required

# データベースを取得して表示する
@login_required
def list_ques(request):
    survey_field_data = Survey.objects.values()
    listdict = {
        'title':'一覧',
        'val':survey_field_data,
    }
    return render(request, 'surveys/list_ques.html', listdict)

@login_required
def create_ques(request):
    listdict = {
        'title':'新規作成画面',
    }
    if request.method == 'POST':
        print("POSTデータ:", request.POST)
        existing_question_count = Survey.objects.count()
        next_survey_id = existing_question_count + 1

        survey_title = request.POST.get('title-text')
        survey_create_user = request.user.email

        path = '/list'

        # 新しいSurveyオブジェクトを作成
        if request.POST.get('action') == 'create':
            survey = Survey(
                id=next_survey_id,
                title=survey_title,
                create_at=timezone.now(),
                create_user=survey_create_user,
                published_flag=True,
                deleted_flag=False
            )
            survey.save()
            path = '/al_list'
        elif request.POST.get('action') == 'tem':
            survey = Survey(
                id=next_survey_id,
                title=survey_title,
                create_at=timezone.now(),
                create_user=survey_create_user,
                published_flag=False,
                deleted_flag=False
            )
            survey.save()
            path = '/tem_list'

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
            existing_question_count = Question.objects.count()
            next_question_id = existing_question_count + 1

            question_type_text = question_types[i]
            question_type = Choicetype.objects.get(type=question_type_text)  

            # Questionオブジェクトの作成
            question = Question(
                id=next_question_id,
                title=question_titles[i],
                survey=survey,
                type=question_type,
                deleted_flag=False
            )
            question.save()

            # テキストボックスじゃない場合に選択肢を取得
            if question_type_text != 'textarea':
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
                        existing_question_count = Choice.objects.count()
                        next_choice_id = existing_question_count + 1

                        choice = Choice(
                            id=next_choice_id,
                            text=choice_text,
                            question=question,
                            deleted_flag=False
                        )
                        choice.save()
        return redirect(path)
    return render(request, 'surveys/create_ques.html', listdict)

@login_required
def al_list(request):
    survey_field_data = Survey.objects.filter(published_flag=True)
    listdict = {
        'title':'公開済みアンケート一覧',
        'val':survey_field_data,
    }
    return render(request, 'surveys/al_list.html', listdict)

@login_required
def tem_list(request):
    survey_field_data = Survey.objects.filter(published_flag=False)
    listdict = {
        'title':'下書きアンケート一覧',
        'val':survey_field_data,
    }
    return render(request, 'surveys/tem_list.html', listdict)

@login_required
def ag_data(request, survey_id):
    survey = Survey.objects.get(id=survey_id)
    # Surveyに関連するQuestionを取得
    questions = Question.objects.filter(survey=survey, deleted_flag=False)
    
    # 各Questionに関連するAnswerを取得して辞書に格納
    question_answers = {}
    for question in questions:
        answers = Answer.objects.filter(question=question)
        # 回答内容をIDからテキストに変換
        formatted_answers = []
        for answer in answers:
            content_list = []
            if question.type.type == "checkbox" or question.type.type == "radio" or question.type.type == "pulldown":
                # 選択肢のIDを選択肢テキストに変換
                for choice_id in answer.context.get("content", []):
                    try:
                        choice = Choice.objects.get(id=choice_id)
                        content_list.append(choice.text)
                    except Choice.DoesNotExist:
                        content_list.append("選択肢が見つかりません")
            else:
                # テキストボックスの場合はそのまま表示
                content_list = answer.context.get("content", [])
                
            formatted_answers.append(content_list)
        
        question_answers[question] = formatted_answers

    context = {
        'survey': survey,
        'question_answers': question_answers,
    }
    
    return render(request, 'surveys/ag_data.html', context)

@login_required
def edit_ques(request, survey_id):
    survey = Survey.objects.get(id = survey_id)
    listdict = {
        'title':'編集画面',
        'survey':survey,
    }
    return render(request, 'surveys/edit_ques.html', listdict)

@login_required
def answer(request, survey_id):
    try:
        # Surveyと関連したQuestionを取り出す
        survey = Survey.objects.get(id=survey_id)
        questions = Question.objects.filter(survey__id=survey_id)
    except Survey.DoesNotExist:
        raise Http404("Survey does not exist")
    
    # GETリクエスト: 回答画面を表示する
    listdict = {
        "survey": survey,
        "question": questions,
        "title": survey.title,
    }
    return render(request, "answers/answer.html", listdict)

@login_required
@csrf_exempt  # CSRF保護を一時的に無効にする（開発中のみ）
def complete(request):
    if request.method == 'POST':
        responses = request.POST
        response_list = []

        for key in responses:
            if key != 'csrfmiddlewaretoken':
                question_id = int(key.replace("answer_", ""))
                question = Question.objects.get(id=question_id)  # 質問を取得
                
                if question.type.type == "checkbox":
                    # チェックボックス形式の質問の場合、複数選択肢をリストとして取得
                    user_answers = request.POST.getlist(key)
                else:
                    # テキストボックスやその他の形式の質問の場合
                    user_answers = [responses[key].strip()]  # 空白を除去

                # 回答が空の場合は保存せずスキップ
                if not any(user_answers):  # user_answersが空リストまたは空文字のみならスキップ
                    continue

                answer_data = {
                    "question_id": question.id,
                    "type": question.type.type,
                    "content": user_answers,  # リスト形式で回答内容を格納
                }

                # Answerインスタンスを作成
                answer_instance = Answer(
                    context=answer_data,  # JSONデータをcontextに格納
                    question=question  # Questionを関連付け
                )
                answer_instance.save()  # データベースに保存
                response_list.append(answer_data)

        # 完了画面に表示するためのデータをレンダリング
        listdict = {
            'title': '回答完了画面',
            'responses': response_list,
        }
        return render(request, 'answers/complete.html', listdict)

    return render(request, 'answers/answer.html', {'title': '回答ページ'})
