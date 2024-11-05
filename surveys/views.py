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