from django.urls import path

from user.views import SignUpView

urlpatterns = [
    path('/join_method', SignUpView.as_view()),
]
