from django.urls import path
from .views     import ReviewView, ProductLikeView, ProductView

urlpatterns = [
    path('/review', ReviewView.as_view()),
    path('/review/<int:product_id>', ReviewView.as_view()),
    path('/like', ProductLikeView.as_view()),
]