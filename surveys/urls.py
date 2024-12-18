from django.urls import path

from . import views

app_name = 'templates'

urlpatterns = [
    path('', views.list_ques, name='list_ques'),
    path('create_ques/', views.create_ques, name='create_ques'),
    path('al_list/', views.al_list, name='al_list'),
    path('tem_list/', views.tem_list, name='tem_list'),
    path('ag_data/<int:survey_id>/', views.ag_data, name='ag_data'),
    # path('al_list/ag_data/<int:survey_id>/', views.ag_data, name='ag_data'),
    path('tem_list/edit_ques/<int:survey_id>/', views.edit_ques, name='edit_ques'),
    path('answer/<int:survey_id>/', views.answer, name='answer'),
    path('complete/<int:survey_id>/', views.complete, name='complete'),
    path('delete_ques/<int:survey_id>', views.delete_ques, name='delete_ques'),
]
