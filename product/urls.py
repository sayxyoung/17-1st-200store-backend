from django.urls   import path

from .views import ProductLikeView

urlpatterns = [
    path('/productlike', ProductLikeView.as_view()),
    path('/productlike/<int:user_id>', ProductLikeView.as_view())
]
