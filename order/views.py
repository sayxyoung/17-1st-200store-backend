import json
from datetime       import datetime, timedelta

from django.http    import JsonResponse
from django.views   import View
from django.utils   import timezone

from order.models   import Order, Cart
from product.models import MatchingReview
from utils          import login_decorator

class OrderListView(View):
    @login_decorator
    def get(self, request):
        data   = json.loads(request.body)
        
        compare_date = timezone.localtime() - timedelta(days=7)
        start_date   = request.GET.get('startDate', compare_date)
        end_date     = request.GET.get('endDate', timezone.localtime())

        orders = Order.objects.filter(user_id=request.user.id, create_at__range=(start_date, end_date))
        
        result = [{
            'serialNumber' : order.serial_number,
            'orderStatus'  : order.status,
            'orderDate'    : order.create_at,
            'orderId'      : order.id,
            'subProducts'  : [{
                'id'            : cart.product.id,
                'name'          : cart.product.name,
                'totalPrice'    : cart.total_price,
                'quantity'      : cart.quantity,
                'productStatus' : cart.status,
                'isReview'      : True if is_review.exists() else False
            } for cart in Cart.objects.filter(order_id=order.id)]
        } for order in orders]

        return JsonResponse({'message':'SUCCESS', 'data': result}, status=200)
