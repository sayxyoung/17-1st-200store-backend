from django.urls import path

from order.views import OrderListView 

urlpatterns = [
    path('/order_list', OrderListView.as_view())
]