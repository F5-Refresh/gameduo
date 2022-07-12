from django.urls import path
from user.views.user_search import UserSearchView

urlpatterns = [
    path('/search/<str:user_id>', UserSearchView.as_view()),
]
