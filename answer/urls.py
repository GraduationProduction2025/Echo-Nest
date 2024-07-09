from django.urls import path
from . import views

urlpatterns = [
    path('survey-result/', views.survey_result, name='survey-result'),
    path('survey-data/', views.survey_data, name='survey-data'),
]