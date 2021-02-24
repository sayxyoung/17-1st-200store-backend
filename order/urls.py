from django.urls import path

from order.views import CartView

urlpatterns = [
    path('/cart', CartView.as_view()),
]
