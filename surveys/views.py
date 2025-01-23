from django.shortcuts import render, redirect
from .models import Survey, Question, Choice, Choicetype, Answer, UsersAnswer
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import datetime, timedelta
import re
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

# データベースを取得して表示する
@login_required
def list_ques(request):
    login_user = request.user.email
    current_time = timezone.now()
    survey_field_data = Survey.objects.exclude(create_user=login_user).filter(published_flag=True, deleted_flag=False, for_publish__gt=current_time)
    query = request.GET.get('query', '')
    if query:
        survey_field_data = survey_field_data.filter(title__icontains=query)
        
    listdict = {
        'title':'一覧',
        'val':survey_field_data,
    }
    return render(request, 'surveys/list_ques.html', listdict)

@login_required
def create_ques(request):
    listdict = {
        'title':'新規作成',
    }
    if request.method == 'POST':
        print("POSTデータ:", request.POST)
        existing_question_count = Survey.objects.count()
        next_survey_id = existing_question_count + 1

        survey_title = request.POST.get('title-text')
        survey_create_user = request.user.email

        path = '/list'

        #公開期間が設定されなかった場合の値
        default_for_publish = timezone.now() + timedelta(days=365*100)

        get_for_publish = request.POST.get('publish_date', '')
        print("publishデータ:", get_for_publish)
        #空文字かどうかをチェック
        if get_for_publish:
            try:
                for_publish = get_for_publish
            except:
                for_publish = default_for_publish
        else:
            for_publish = default_for_publish


        # 新しいSurveyオブジェクトを作成
        if request.POST.get('action') == 'create':
            survey = Survey(
                id=next_survey_id,
                title=survey_title,
                create_at=timezone.now(),
                create_user=survey_create_user,
                for_publish=for_publish,
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
                for_publish=default_for_publish,
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

            # 画像の処理
            image_file = request.FILES.get(f'ques-image-{i + 1}')
            if image_file:
                # 画像がアップロードされた場合
                new_filename = f"img-{question.id}.{image_file.name.split('.')[-1]}"
                image_path = f"question_images/{new_filename}"
                saved_path = default_storage.save(image_path, ContentFile(image_file.read()))
                
                # 画像パスをQuestionに保存
                question.image = saved_path
                question.save()
            else:
                question.image = "none"
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
    login_user = request.user.email
    survey_field_data = Survey.objects.filter(create_user=login_user, published_flag=True, deleted_flag=False)
    listdict = {
        'title':'公開済みアンケート一覧',
        'val':survey_field_data,
    }
    return render(request, 'surveys/al_list.html', listdict)

@login_required
def tem_list(request):
    login_user = request.user.email
    survey_field_data = Survey.objects.filter(create_user=login_user, published_flag=False, deleted_flag=False)
    listdict = {
        'title':'下書きアンケート一覧',
        'val':survey_field_data,
    }
    return render(request, 'surveys/tem_list.html', listdict)

@login_required
def ag_data(request, survey_id):
    # 対象のSurveyを取得
    survey = Survey.objects.get(id=survey_id)

    # Surveyに関連するQuestionを取得
    questions = Question.objects.filter(survey=survey, deleted_flag=False)

    # JSONデータの格納先
    answer_data = []
    # JSONデータのid
    answer_id = 0

    # 各Questionに関連するデータを処理
    for question in questions:
        answers = Answer.objects.filter(question=question)
        
        # 選択式質問の場合
        if question.type.type in ["checkbox", "radio", "select"]:
            choice_counts = {}  # 選択肢の集計用辞書

            # 各回答を解析
            for answer in answers:
                for choice_id in answer.context.get("content", []):
                    try:
                        choice = Choice.objects.get(id=choice_id)
                        if choice.text not in choice_counts:
                            choice_counts[choice.text] = 0
                        choice_counts[choice.text] += 1
                    except Choice.DoesNotExist:
                        if "選択肢が見つかりません" not in choice_counts:
                            choice_counts["選択肢が見つかりません"] = 0
                        choice_counts["選択肢が見つかりません"] += 1

            # データを追加
            answer_data.append({
                'id': answer_id,
                'question': question.title,
                'labels': list(choice_counts.keys()),
                'data': list(choice_counts.values()),
                'total_votes': sum(choice_counts.values())
            })
            answer_id += 1
        # テキスト形式の場合
        elif question.type.type in ["textarea"]:
            text_answers = []
            # 回答をすべて取り出す
            for answer in answers:
                content = answer.context.get("content", [])
                if isinstance(content, list):
                    text_answers.extend(content)
                elif isinstance(content, str):
                    text_answers.append(content)
            # データを追加
            answer_data.append({
                'id':answer_id,
                'question': question.title,
                'responses': text_answers,
            })
            answer_id += 1
        # その他の場合はelifで追記
        else:
            pass
    listdict = {
        'title':'アンケート結果ダッシュボード',
        'context':answer_data,
    }
    return render(request, 'surveys/ag_data.html', listdict)

@login_required
def edit_ques(request, survey_id):
    try:
        # Surveyと関連したQuestionを取り出す
        survey = Survey.objects.get(id=survey_id)
        questions = Question.objects.filter(survey=survey)
        choices = Choice.objects.filter()
    except Survey.DoesNotExist:
        raise Http404("Survey does not exist")

    if request.method == 'POST':
        print("POSTデータ:", request.POST)
        existing_question_count = Survey.objects.count()
        next_survey_id = existing_question_count + 1

        survey_title = request.POST.get('title-text')
        survey_create_user = request.user.email

        path = '/list'

        #公開期間が設定されなかった場合の値
        default_for_publish = timezone.now() + timedelta(days=365*100)

        # 新しいSurveyオブジェクトを作成
        if request.POST.get('action') == 'create':
            survey = Survey(
                id=next_survey_id,
                title=survey_title,
                create_at=timezone.now(),
                for_publish=default_for_publish,
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
                for_publish=default_for_publish,
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
        survey = Survey.objects.get(id=survey_id)
        survey.deleted_flag = True
        survey.save()
        return redirect(path)
    listdict = {
        'title':'アンケート編集',
        'survey':survey,
        'question':questions,
        'choice':choices,
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
def complete(request, survey_id):
    if request.method == 'POST':
        responses = request.POST
        response_list = []

        # Survey ID を取得（仮定としてフォームに survey_id を含める）
        survey_id = int(request.POST.get("survey_id"))
        survey = Survey.objects.get(id=survey_id)  # アンケートを取得

        for key in responses:
            if key != 'csrfmiddlewaretoken' and key != 'survey_id':
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

        # ユーザの回答記録をデータベースに追加
        if not UsersAnswer.objects.filter(user=request.user, answered_survey=survey).exists():
            user_answer = UsersAnswer(
                user=request.user,
                answered_survey=survey
            )
            user_answer.save()

        # 完了画面に表示するためのデータをレンダリング
        listdict = {
            'title': '回答が完了しました。',
            'responses': response_list,
            'survey_num': survey_id,  # survey_idをテンプレートに渡す
        }
        return render(request, 'answers/complete.html', listdict)

    return redirect('templates:answer', survey_id=survey_id)

@login_required
def answered(request):
    # ログインしているユーザが回答したアンケートのうち削除済みでないものを表示
    usersanswer = UsersAnswer.objects.filter(user = request.user, answered_survey__deleted_flag=False)
    listdict = {
        'title': '回答済みアンケート一覧',
        'answered': usersanswer,
    }
    return render(request, 'surveys/answered_list.html', listdict)

@login_required
def deleted(request):
    # ログインしているユーザが回答したアンケートのうち削除済みのものを表示
    deletedanswer = UsersAnswer.objects.filter(user = request.user, answered_survey__deleted_flag=True)
    listdict = {
        'title': '削除されたアンケート一覧',
        'deleted': deletedanswer,
    }
    return render(request, 'surveys/deleted_list.html', listdict)

def publish_ques(request, survey_id):
    survey = Survey.objects.get(id=survey_id)
    survey.published_flag=True
    survey.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def delete_ques(request, survey_id):
    survey = Survey.objects.get(id=survey_id)
    survey.deleted_flag=True
    survey.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))