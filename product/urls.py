from django.urls   import path

from .views import ProductLikeView

urlpatterns = [
    path('/product_like', ProductLikeView.as_view()),
    path('/product_like/<int:user_id>', ProductLikeView.as_view())
]
