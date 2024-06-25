from django.urls import path

from . import views

app_name = 'templates'

urlpatterns = [
    path('list/', views.list, name='list'),
    path('detail/<int:survey_id>/', views.detail, name='detail'),
    path('add/', views.add, name='add'),
    path('create/', views.create, name='create'),
]
