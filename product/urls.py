from django.urls   import path
from product.views import ProductView ,ReviewView

urlpatterns = [
        path('/product', ProductView.as_view()),
        path('/<int:category_id>', ProductView.as_view()),
        path('/<int:category_id>/<str:sorting>', ProductView.as_view()),
        path('/review', ReviewView.as_view()),
        path('/review/<int:product_id>', ReviewView.as_view())
]
