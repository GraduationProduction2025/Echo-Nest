from django.urls import path
from . import views

app_name = 'templates'

urlpatterns = [
    path('list/', views.index, name='list'),
    path('delete/', views.delete_surveys, name='delete'),
]
