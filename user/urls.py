from django.urls import path

from user.views import SignInView

urlpatterns = [
    path('/login', SignInView.as_view()),
]