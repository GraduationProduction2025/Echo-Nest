from django.urls import include, path

from . import views

app_name = "accounts"

urlpatterns = [
    # path("", views.index),
    # path('', include('surveys.urls')),
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout")
]