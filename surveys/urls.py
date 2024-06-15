from django.urls import path

from . import views

app_name = 'templates'

urlpatterns = [
    path('list/', views.index, name='list'),
    path('info/', views.info, name='info'),
    path('detail/', views.detail_view, name='detail'),
    path('add/', views.add, name='add'),
    path('create/', views.create, name='create'),
    path('test/', views.test, name='test'),
    path('testcreate/', views.testcreate, name='testcreate'),
]
