from django.urls   import path

from .views import ProductLikeView

urlpatterns = [
    path('/productLike', ProductLikeView.as_view()),
    path('/productLike/<int:user_id>', ProductLikeView.as_view())
]
