from django.urls   import path

from .views import ProductLikeView

urlpatterns = [
    path('/like', ProductLikeView.as_view()),
]
