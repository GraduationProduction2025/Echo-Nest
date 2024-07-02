from django.shortcuts import render,redirect
from .models import Survey, Question, Choice, Choicetype
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .forms import SurveyAddForm, SurveyCreateForm, QuestionCreateForm, ChoiceCreateForm

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
    header = ['ステータス','質問タイトル','作成日','作成ユーザ']
    infodict = {
        'title':'テスト',
        'header':header,
        'val':survey,
        'val2':survey_2,
    }
    return render(request, 'surveys/info.html', infodict)

# データベースの内容を取得して表示
def detail(request):
    survey = Survey.objects.all()
    question = Question.objects.all()
    choicetype = Choicetype.objects.all()
    choice = Choice.objects.all()
    header = ['ステータス','質問タイトル','URL','作成日','作成ユーザ']
    detaildict = {
        'title':'アンケート詳細',
        'header':header,
        'survey':survey,
        'q':question,
        'c':choice,
        'ct':choicetype,
    }
    return render(request, 'surveys/detail.html', detaildict)

# テスト
def add(request):
    base = {
        'title':'アンケート追加'
    }
    return render(request,'surveys/add.html',base)
    # return HttpResponse('add')

# def create(request):
#     base = {
#     'title':'アンケート作成'
#     }
#     # return render(request,'surveys/create.html',base)
#     return HttpResponse('create')

def create(request):
    if request.method == 'POST':
        form = SurveyAddForm(request.POST)
        if form.is_valid():
            survey = Survey()
            survey.id = form.cleaned_data['id']
            survey.title = form.cleaned_data['title']
            survey.url = form.cleaned_data['url']
            survey.create_at = form.cleaned_data['create_at']
            survey.create_user = form.cleaned_data['create_user']
            survey.delete_flag = form.cleaned_data['delete_flag']
            survey.save()
            return redirect('../detail/')

    else:
        form = SurveyAddForm()

    return render(request, 'surveys/create.html', {'form': form})

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

def generate_id(model):
    last_item = model.objects.order_by('id').last()
    if not last_item:
        return 1
    return last_item.id + 1

def test(request):
    if request.method == 'POST':
        survey_form = SurveyCreateForm(request.POST)
        question_form = QuestionCreateForm(request.POST)
        choice_form = ChoiceCreateForm(request.POST)

        if survey_form.is_valid() and question_form.is_valid() and choice_form.is_valid():
            # Surveyを保存
            survey = survey_form.save(commit=False)
            survey.id = generate_id(Survey)
            survey.save()

            # Questionを保存し、Surveyと関連付ける
            question = question_form.save(commit=False)
            question.id = generate_id(Question)
            question.survey = survey
            question.save()

            # Choiceを保存し、Questionと関連付ける
            choice = choice_form.save(commit=False)
            choice.id = generate_id(Choice)
            choice.question = question
            choice.save()

            return redirect('../detail/')

    else:
        survey_form = SurveyCreateForm()
        question_form = QuestionCreateForm()
        choice_form = ChoiceCreateForm()

    return render(request, 'surveys/test.html', {
        'title':'アンケート作成',
        'survey_form': survey_form,
        'question_form': question_form,
        'choice_form': choice_form,
    })

# Create formsets
QuestionFormSet = inlineformset_factory(Survey, Question, form=QuestionCreateForm, extra=1, can_delete=True)
ChoiceFormSet = inlineformset_factory(Question, Choice, form=ChoiceCreateForm, extra=1, can_delete=True)

def create_survey(request):
    if request.method == 'POST':
        survey_form = SurveyCreateForm(request.POST)
        question_formset = QuestionFormSet(request.POST, request.FILES)
        if survey_form.is_valid() and question_formset.is_valid():
            survey = survey_form.save(commit=False)
            survey.id = generate_id(Survey)
            survey.save()
            questions = question_formset.save(commit=False)
            for question in questions:
                question.survey = survey
                question.id = generate_id(Question)
                question.save()

            for form in question_formset.deleted_forms:
                if form.instance.pk:
                    form.instance.delete()

            return redirect('../detail/')  # 適切なリダイレクト先に変更してください
    else:
        survey_form = SurveyCreateForm()
        question_formset = QuestionFormSet()

    return render(request, 'surveys/test2.html', {
        'survey_form': survey_form,
        'question_formset': question_formset,
    })

def edit_survey(request, survey_id):
    survey = Survey.objects.get(pk=survey_id)
    question_formset = QuestionFormSet(request.POST or None, request.FILES or None, instance=survey)
    
    if request.method == 'POST':
        survey_form = SurveyCreateForm(request.POST, instance=survey)
        if survey_form.is_valid() and question_formset.is_valid():
            survey = survey_form.save()
            questions = question_formset.save(commit=False)
            for question in questions:
                question.survey = survey
                if not question.id:
                    question.id = generate_id(Question)
                question.save()

            for form in question_formset.deleted_forms:
                if form.instance.pk:
                    form.instance.delete()

            return redirect('../detail/')  # 適切なリダイレクト先に変更してください

    else:
        survey_form = SurveyCreateForm(instance=survey)

    return render(request, 'surveys/test3.html', {
        'survey_form': survey_form,
        'question_formset': question_formset,
    })