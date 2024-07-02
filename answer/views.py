from django.shortcuts import render
from django.http import JsonResponse

def survey_result(request):
    return render(request, 'answer/survey_result.html')

def survey_data(request):
    # 仮のデータを直接ここで設定
    data = {
        'question': "あなたの好きなプログラミング言語は何ですか？",
        'labels': ['Python', 'JavaScript', 'Java', 'C++', 'Ruby'],
        'data': [30, 25, 20, 15, 10],
        'total_votes': 100
    }
    return JsonResponse(data)