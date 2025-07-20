from django.urls import path
from .views import CartView, LoginView, SignupView

urlpatterns = [
    # sign up flow:
    path("signup/", SignupView.as_view(), name="signup"),

    # login flow:
    path("login/", LoginView.as_view(), name="login"),

    # cart item:
    path("cart/", CartView.as_view(), name="cart"),
]