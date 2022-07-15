from django.urls import include, path

from user.views.signup_view import SignUpView
from user.views.user_search import UserSearchView

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/search/<str:account>', UserSearchView.as_view()),
]
