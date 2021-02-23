from django.urls   import path
from product.views import ProductDetailView, ProductListView, ReviewView

urlpatterns = [
        path('', ProductListView.as_view()),
        path('/<int:product_id>', ProductDetailView.as_view()),
        path('/review', ReviewView.as_view()),
        path('/review/<int:product_id>', ReviewView.as_view())
]
