from django.urls   import path

from .views import ProductLikeView
#from product.views import ProductView

urlpatterns = [
    path('/productLike', ProductLikeView.as_view()),
    # path('/productLike/<int:user_id>', ProductLikeView.as_view())
#        path('/product', ProductView.as_view()),
 #       path('/<str:category>', ProductView.as_view()),
]
