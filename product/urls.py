
from django.urls   import path
from product.views import ProductView

urlpatterns = [
        path('/product', ProductView.as_view()),
        path('/<int:category_id>', ProductView.as_view()),
        path('/<int:category_id>/<str:sorting>', ProductView.as_view()),
]
