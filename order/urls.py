from django.urls import path

<<<<<<< HEAD
from order.views import OrderListView 

urlpatterns = [
    path('', OrderListView.as_view())
=======
from order.views import CartView

urlpatterns = [
    path('/cart', CartView.as_view()),
>>>>>>> main
]