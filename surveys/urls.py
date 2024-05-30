from django.urls import path
from .views import listView

urlpatterns = [
    path("list", listView.as_view()),
]