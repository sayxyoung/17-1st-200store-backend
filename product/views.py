import json

from django.http  import JsonResponse
from django.views import Views

from order.models import Order, Cart

class OrderListView(View):
    def get(self, request):
        pass
    
    def post(self, request):
        data = json.loads(request.body)

        order_list = []
        orders = Order.objects.filter(user_id=data['userId']) # decorator 되면 거기서 받아오기
        
        for order in orders:
            products = Cart.objects.filter(order_id=order.id)
            products = [{
                
            } for product in products]