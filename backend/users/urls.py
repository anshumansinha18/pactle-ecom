from django.urls import path
from .views import LoginView, SignupView

urlpatterns = [
    # sign up flow:
    path("signup/", SignupView.as_view(), name="signup"),

    # login flow:
    path("login/", LoginView.as_view(), name="login"),
]