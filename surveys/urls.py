from django.urls import path

from . import views

app_name = 'templates'

urlpatterns = [
    path('list/', views.index, name='list'),
    path('info/', views.info, name='info'),
]
