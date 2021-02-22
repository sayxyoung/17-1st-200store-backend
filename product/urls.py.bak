
from django.urls   import path
from product.views import ProductDetailView, ProductListView

urlpatterns = [
        path('/product', ProductListView.as_view()),
        path('/goods_list/<int:category_id>', ProductListView.as_view()),
        path('/goods_list/<int:category_id>/<str:sorting>', ProductListView.as_view()),
        path('/goods_view/<int:product_id>', ProductDetailView.as_view()),
]
