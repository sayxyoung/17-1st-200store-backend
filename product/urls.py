from django.urls  import path
from product.view import ProductView, ReviewView

from .views import MainView

urlpatterns = [
    path('/review', ReviewView.as_view()),
    path('/review/<int:product_id>', ReviewView.as_view())
]