from django.urls import path
from .views     import ReviewView
#from product.views import ProductView

urlpatterns = [
    path('/review', ReviewView.as_view()),
    path('/review/<int:product_id>', ReviewView.as_view())
#        path('/product', ProductView.as_view()),
 #       path('/<str:category>', ProductView.as_view()),
]
