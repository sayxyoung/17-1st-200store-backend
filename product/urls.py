
from django.urls   import path
from product.views import ProductDetailView, ProductListView

urlpatterns = [
        path('', ProductListView.as_view()),
        path('/<int:product_id>', ProductDetailView.as_view()),
]
