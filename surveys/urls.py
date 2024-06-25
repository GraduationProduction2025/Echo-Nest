from django.urls import path

from . import views

app_name = 'templates'

urlpatterns = [
    path('list/', views.list, name='list'),
    path('update/<int:survey_id>/', views.update, name='update'),
]
