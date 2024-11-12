from django.shortcuts import render, redirect
from .models import Survey, Question, Choice, Choicetype, Answer
from django.http import HttpResponse, Http404
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt

# データベースを取得して表示する
def list_ques(request):
    survey_field_data = Survey.objects.values()
    listdict = {
        'title':'一覧',
        'val':survey_field_data,
    }
    return render(request, 'surveys/list_ques.html', listdict)

def create_ques(request):
    base = {
    'title':'アンケート作成'
    }
    return render(request,'surveys/create_ques.html',base)

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
    survey = Survey.objects.get(id=survey_id)
    questions = Question.objects.filter(survey=survey, deleted_flag=False)
    
    question_answers = {}
    for question in questions:
        answers = Answer.objects.filter(question=question)
        
        formatted_answers = []
        for answer in answers:
            content_list = []
            if question.type.type in ["checkbox", "radio", "pulldown"]:
                for choice_id in answer.context.get("content", []):
                    try:
                        choice = Choice.objects.get(id=choice_id)
                        if choice.text:  # 空文字でないかチェック
                            content_list.append(choice.text)
                    except Choice.DoesNotExist:
                        content_list.append("選択肢が見つかりません")
            else:
                # テキストボックスの場合も空文字を除外
                content = answer.context.get("content", [])
                if content:
                    content_list.extend([text for text in content if text])  # 空文字でないものだけ追加

            if content_list:  # 空リストでない場合のみ追加
                formatted_answers.append(content_list)
        
        question_answers[question] = formatted_answers

    context = {
        'survey': survey,
        'question_answers': question_answers,
    }
    
    return render(request, 'surveys/ag_data.html', context)



def edit_ques(request, survey_id):
    survey = Survey.objects.get(id = survey_id)
    listdict = {
        'title':'編集画面',
        'survey':survey,
    }
    return render(request, 'surveys/edit_ques.html', listdict)

def answer(request, survey_id):
    try:
        # Surveyと関連したQuestionを取り出す
        survey = Survey.objects.get(id=survey_id)
        questions = Question.objects.filter(survey__id=survey_id)
    except Survey.DoesNotExist:
        raise Http404("Survey does not exist")

    if request.method == "POST":
        # POSTリクエスト: 回答データを保存する
        for question in questions:
            # `answer_<question_id>`という名前で回答が送信されているかを確認
            answer_key = f'answer_{question.id}'
            if question.type.type == "text":
                # テキスト回答の場合
                user_answer = request.POST.get(answer_key, "")
                if user_answer:  # 入力がある場合のみ保存
                    Answer.objects.create(
                        context={'text': user_answer},
                        question=question,
                    )
            elif question.type.type == "checkbox":
                # チェックボックス回答の場合
                user_answers = request.POST.getlist(answer_key)  # 複数選択肢
                if user_answers:  # 選択肢がある場合のみ保存
                    Answer.objects.create(
                        context={'choices': user_answers},
                        question=question,
                    )
        # 回答完了後にリダイレクト
        return redirect('/complete/')

    # GETリクエスト: 回答画面を表示する
    listdict = {
        "survey": survey,
        "question": questions,
        "title": survey.title,
    }
    return render(request, "answers/answer.html", listdict)


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
                    user_answers = [responses[key]]

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