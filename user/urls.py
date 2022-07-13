from django.urls import include, path

<<<<<<< HEAD
from user.views.signup_view import SignUpView

urlpatterns = [
    path('/signup',SignUpView.as_view())
=======
urlpatterns = [
    #  path('accounts/', include('dj_rest_auth.registration.urls')),
>>>>>>> 38910fb (로그인 시리얼라이저 추가 (#4))
]
