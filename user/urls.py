from django.urls import include, path

from user.views.signup_view import SignUpView

urlpatterns = [
    path('/signup',SignUpView.as_view())
]
